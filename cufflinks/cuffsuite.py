"""Contains a wrapper for reading and returning a python interpretation of a CuffLinks
Output.

Written by Kevin Wu, Ortiz Lab, September 2015"""
import sys, subprocess, glob, os
sys.path.append(os.environ['PIPELINEHOME'] + "/util/") # Use environment variable to be flexible ond different systems
import fileUtil as f
import shellUtil as s
import re
import numpy as np
from collections import namedtuple
import csv

def readCufflinksTranscriptsGtf(cfFilename):
    transcript = namedtuple('transcript', 'chr start end gene_id transcript_id FPKM frac')
    # def extractFromQuotes(x):
    #     indices = [m.start() for m in re.finditer('"', x)]
    #     return x[indices[0]+1:indices[1]]
    transcriptDict = {}
    cfFile = open(cfFilename)
    for line in cfFile:
        tokenized = line.rstrip().split('\t')
        if tokenized[2] == 'transcript': #Wait what....
            continue
        chromosome = tokenized[0]
        start = tokenized[3]
        end = tokenized[4]
        tokenized2 = tokenized[8].split(';')
        gene = f.extractFromQuotes(tokenized2[0])
        t = f.extractFromQuotes(tokenized2[1])
        fpkm = float(f.extractFromQuotes(tokenized2[3]))
        frac = f.extractFromQuotes(tokenized2[4])
        thisLineObject = transcript(chromosome, start, end, gene, t, fpkm, frac)
        transcriptDict[t] = thisLineObject
    cfFile.close()
    return transcriptDict

def readCufflinksIsoformsFPKM(filename):
    """Reads a """
    # isoform = namedtuple('isoform', 'tracking_id gene_id gene_short_name tss_id length coverage FPKM')
    isoform = namedtuple('isoform', 'tracking_id class_code nearest_ref_id gene_id gene_short_name tss_id locus length coverage FPKM FPKM_conf_lo FPKM_conf_hi FPKM_status')
    isoformsDict = {}
    if "isoforms.fpkm_tracking" in filename:
        file = open(filename)
        for line in file:
            if "tracking_id" == line[:11]:
                continue
            tokenized = line.rstrip().split('\t')
            tid = tokenized[0]
            # gid = tokenized[3]
            # gShortName = tokenized[4]
            # tssId = tokenized[5]
            # l = tokenized[7]
            # cov = tokenized[8]
            # fpkm = float(tokenized[9])
            # thisLineObject = isoform(tid, gid, gShortName, tssId, l, cov, fpkm)
            thisLineObject = isoform(*tokenized)
            isoformsDict[tid] = thisLineObject
        file.close()
        return isoformsDict
    else:
        print("This is not a isoforms.fpkm_tracking file")
        return None

def readCufflinksGenesFPKM(filename):
    # Each gene is a dictionary key, mapping to a named tuple of properties.
    # This dictionary is then returned. 
    # gene = namedtuple('gene', 'tracking_id gene_id gene_short_name tss_id FPKM')
    gene = namedtuple('gene', 'tracking_id class_code nearest_ref_id gene_id gene_short_name tss_id locus length coverage FPKM FPKM_conf_lo FPKM_conf_hi FPKM_status')
    genesDict = {}
    if "genes.fpkm_tracking" in filename:
        file = open(filename)
        for line in file:
            if "tracking_id" == line[:11]:
                continue
            tokenized = line.rstrip().split('\t')
            tid = tokenized[0]
            thisLineObject = gene(*tokenized)
            genesDict[tid] = thisLineObject
        file.close()
        return genesDict
    else:
        print("This is not a genes.fpkm_tracking file")
        return None

def aggregateCufflinksResults():
    """Visits all the cufflinks results folders, and aggregate both the genes and transcripts
    files into a .csv file. This implementation ignores all the given confience intervals."""
    genesResults, transcriptsResults = {}, {}
    cufflinksDirs = glob.glob('*_cufflinks')
    for d in cufflinksDirs:
        genesResult = readCufflinksGenesFPKM(d + '/genes.fpkm_tracking')
        transcriptsResult = readCufflinksIsoformsFPKM(d + '/isoforms.fpkm_tracking')
        # INSERT HERE
        sampleName = d[:-10] # Remove the '_cufflinks' folder suffix to get the sample name
        # Make sure the sample is not a duplicate
        assert sampleName not in genesResults
        assert sampleName not in transcriptsResults
        genesResults[sampleName] = genesResult
        transcriptsResults[sampleName] = transcriptsResult
    # sanity check the results that every result file has the same genes/transcripts
    for result in genesResults:
        for gene in result.keys():
            assert gene in genesResults[0].keys()
    for result in transcriptsResults:
        for transcript in result.keys():
            assert transcript in transcriptsResults[0].keys()
    # Write to .csv
    genesFilename, transcriptsFilename = 'aggregated_genes_FPKM.csv', 'aggregated_transcripts_FPKM.csv'
    genesFile = open(genesFilename, mode = 'w')
    genesHeader = 'sample,' + ','.join(genesResults[0].keys()) + "\n"
    genesFile.write(genesHeader)
    for sample in genesResults: # Sample is a string of the sample
        lineItems = [sample]
        result = genesResults[sample]
        for gene in result.keys():
            lineItems.append(result[gene])
        genesFile.write(','.join(lineItems) + '\n`')
    genesFile.close()

    transcriptsFile = open(transcriptsFilename, mode = 'w')
    transcriptsHeader = 'sampmle,' + ','.join(transcriptsResults[0].keys()) + '\n'
    transcriptsFile.write(transcriptsHeader)
    for sample in transcriptsResults:
        lineItems = [sample]
        result = transcriptsResults[sample]
        for t in result.keys():
            lineItems.append(result[t])
        transcriptsFile.write(','.join(lineItems) + '\n')
    transcriptsFile.close()
    return None

def summarizeCufflinksResults(mode, referenceGTF, outputFile = None):
    assert "gtf" in referenceGTF
    def uniqueIDsInRefGTF(m, rGTF):
        x = open(rGTF)
        IDs = set()
        for line in x:
            ID = ""
            if m == "transcripts":
                ID = f.extractFromQuotes(line.split('\t')[8].split(';')[1])
                assert "TCONS" in ID
            else:
                ID = f.extractFromQuotes(line.split('\t')[8].split(';')[0])
                assert "XLOC" in ID
            IDs.add(ID)
        x.close()
        return(IDs)

    # Gather the results
    mode = mode.lower()
    cufflinksDirs = glob.glob("*_cufflinks")
    allOutputs = []
    if mode == "genes":
        for directory in cufflinksDirs: # Read in every cufflinks result
            filename = directory + '/genes.fpkm_tracking'
            allOutputs.append(readCufflinksGenesFPKM(filename))
    elif mode == "transcripts":
        for directory in cufflinksDirs:
            filename = directory + '/isoforms.fpkm_tracking'
            allOutputs.append(readCufflinksIsoformsFPKM(filename))
    else:
        print("Mode must either be genes or transcripts.")
        return None
    
    IDs = uniqueIDsInRefGTF(mode, referenceGTF)
    aggregatedResults = {}
    for ID in IDs:
        listOfFPKMS = []
        for o in allOutputs:
            fpkm = float(o[ID].FPKM)
            listOfFPKMS.append(fpkm)
        aggregatedResults[ID] = listOfFPKMS

    # Aggrgate and write the results
    if outputFile == None:
        outputFile = "aggregated_%s_results.txt" % mode
    output = open(outputFile, 'w')
    header = "%s\tSamples_Above_0.2\tPercent_Samples_Above_0.2\tAverage_FPKM\tMedian_FPKM\n"
    if mode == "genes":
        header = header % "Gene"
    else:
        header = header % "Transcript"
    output.write(header)

    for key in aggregatedResults:
        data = aggregatedResults[key]
        dataTrim = [x for x in data if x > 0.2]
        mean = np.mean(data)
        med = np.median(data)
        output.write("%s\t%s\t%s\t%s\t%s\n" % (key, len(dataTrim), float(len(dataTrim))/float(len(data)), mean, med))
    output.close()


def aggregateAllCufflinksTranscriptResultsDEPRECATED(referenceGTF, outputFile = "aggregated_transcript_results.txt"):
    cufflinksDirs = glob.glob("*_cufflinks")
    allOutputs = []
    for directory in cufflinksDirs:
        filename = directory + '/transcripts.gtf'
        allOutputs.append(readCufflinksOutput(filename))
    refGTF = open(referenceGTF)
    aggregatedResults = {}
    for line in refGTF: #Walk through the reference GTF, and aggregate results for each transcript
        tcon = f.extractFromQuotes(line.split('\t')[8].split(';')[1])
        listOfFPKMS = []
        for o in allOutputs:
            fpkm = float(o[tcon].FPKM)
            listOfFPKMS.append(fpkm)
        aggregatedResults[tcon] = listOfFPKMS
    refGTF.close()

    output = open(outputFile, 'w')
    output.write("Transcript\tSamples_Above_0.2\tPercent_Samples_Above_0.2\tAverage_FPKM\tMedian_FPKM\n")
    for key in aggregatedResults:
        data = aggregatedResults[key]
        dataTrim = [x for x in data if x > 0.2]
        mean = np.mean(data)
        med = np.median(data)
        output.write("%s\t%s\t%s\t%s\t%s\n" % (key, len(dataTrim), float(len(dataTrim))/float(len(data)), mean, med))
    output.close()




# test = readCufflinksOutput("/Users/kevin/Desktop/transcripts.gtf")
# print(test["TCONS_00001875"].FPKM)
# Establish a dictionary, keys are lncRNAs, items are counts of occurences > 0.2 fpkm
# Second dictionary, keys are lncRNAs, items is list of fpkm

# Looks like we want the XLOC one (gene id)