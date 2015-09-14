"""Contains a wrapper for reading and returning a python interpretation of a CuffLinks
Output.

Written by Kevin Wu, Ortiz Lab, September 2015"""
import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
# import fileUtil as f
# import shellUtil as s
import re
from collections import namedtuple

def readCufflinksOutput(cfFilename):
    transcript = namedtuple('transcript', 'chr start end gene_id transcript_id FPKM frac')
    def extractFromQuotes(x):
        indices = [m.start() for m in re.finditer('"', x)]
        return x[indices[0]+1:indices[1]]
    transcriptDict = {}
    cfFile = open(cfFilename)
    for line in cfFile:
        tokenized = line.rstrip().split('\t')
        if tokenized[2] == 'transcript':
            continue
        chromosome = tokenized[0]
        start = tokenized[3]
        end = tokenized[4]
        tokenized2 = tokenized[8].split(';')
        gene = extractFromQuotes(tokenized2[0])
        t = extractFromQuotes(tokenized2[1])
        fpkm = extractFromQuotes(tokenized2[3])
        frac = extractFromQuotes(tokenized2[4])
        thisLineObject = transcript(chromosome, start, end, gene, t, fpkm, frac)
        transcriptDict[t] = thisLineObject
    cfFile.close()
    return transcriptDict

# test = readCufflinksOutput("/Users/kevin/Desktop/transcripts.gtf")
# print(test["TCONS_00001875"].FPKM)
# Establish a dictionary, keys are lncRNAs, items are counts of occurences > 0.2 fpkm
# Second dictionary, keys are lncRNAs, items is list of fpkm

# Looks like we want the XLOC one (gene id)