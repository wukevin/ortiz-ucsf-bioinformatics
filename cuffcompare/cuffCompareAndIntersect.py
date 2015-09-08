"""
This script automates the process of comparing either two or three .gtf
transcript files using CuffCompare. First, we run all pairwise comparisons
between the gtf files given, because CuffCompare does non-symmetric comparisons.
If there are 3 files, there will be 6 comparisons, and 2 files, 4 comparisons.
After running cuffcompare, we take all the results, and take an intersection
of transcipts called by 2 or more tools by taking an union of the following:
Transfrag code | Keep Reference? | Keep Query?
       c       |       yes       |     no
       =       |       yes       |     no
       j       |       yes       |     yes
We then take all the unique transcripts, and construct a final file called
xxx_intersected_transcripts.gtf by pulling from the original .gtf files. To
generate this final file, the input .gtf files must be named in the following
format: CellLine_TranscriptConstructionTool_Transcripts.gtf
For example: FOM_E_Stringtie_Transcripts.gtf
This can be achieved using the Linux "rename" command.
Example usage:
python cuffCompareAndIntersect AV1_N_Cufflinks_Transcripts.gtf AV1_N_Trinity_Transcripts.gtf

Author: Kevin Wu - Ortiz Lab, UCSF - August 2015
"""

import subprocess
import sys
import re
import os
import time

def getToolFromFilename(f, delim = "_"):
    splitted = f.split(delim)
    tool = splitted[len(splitted)-2]
    return tool

def getCellLineFromFilename(f, delim = "_"):
    splitted = f.split(delim)
    b = max([splitted.index(x) for x in ["Trinity", "Cufflinks", "Stringtie"] if x in splitted])
    line = "_".join(splitted[0:b])
    return line

def getTranscriptID(longstring):
    # Given a token from a .tracking file (or any string), extracts transcript ID
    # Examples of what we're looking for
    # Trinity: align_id:160849|GG14081
    # Cufflinks: CUFF.54.1
    # Stringtie: STRG.4.1
    if "CUFF" in longstring:
        match = re.search(r'CUFF\.[0-9]*\.[0-9]*', longstring)
    elif "STRG" in longstring:
        match = re.search(r'STRG\.[0-9]*\.[0-9]*', longstring)
    elif "GG" in longstring and "align_id:" in longstring:
        # Maybe GG is just because Genome-Guided? Maybe not best indentifier
        match = re.search(r'align_id:[0-9]*\|GG[0-9]*',longstring)
    else:
        print("WARNING: Failed to find transcript ID in following string:")
        print(longstring)
        return None
    return match.group(0)

def runCuffDiff(*args):
    # Runs cuffdiff on the given gtf files, alternating using one as reference
    # and one as the query. Can handle either 2 or 3 .gtf files. Writes a log of
    # commands executed.
    commandTemplate = "cuffcompare -s /media/rawData/genomes/GATK_hg19/hg19/ucsc.hg19.fasta -o %s -r %s %s"
    prefixTemplate = "%s_%s_vs_%s_ref"
    commands = []
    trackingFiles = []
    if (len(args) < 4 and len(args) > 1):
        if len(args) == 2:
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[0]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[0], args[1]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[1]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[1], args[0]))
        elif len(args) == 3:
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[0]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[0], args[1]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[2]), getToolFromFilename(args[0]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[0], args[2]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[1]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[1], args[0]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[2]), getToolFromFilename(args[1]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[1], args[2]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[2]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[2], args[0]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[2]))
            trackingFiles.append(prefix+".tracking")
            commands.append(commandTemplate % (prefix, args[2], args[1]))
    else:
        print("This program takes 2 or 3 input arguments. Each input must be a .gtf")
        print("file. We then use CuffCompare to do pairwise comparisons and return")
        print("a final merged .gtf. Order of input does not matter. Example:")
        print("python cuffCompareAndIntersect AV1_N_Cufflinks_Transcripts.gtf AV1_N_Trinity_Transcripts.gtf")
        exit()
    filename = getCellLineFromFilename(args[0]) + "_cuffcompare_commands.log"
    f = open(filename, mode = "w") # This is the log of commands
    for command in commands:
        subprocess.call(command, shell = True)
        f.write(command + "\n")
    f.close()
    return trackingFiles

def extractIDsFromTrackingFile(filename):
    # Tab-delimited
    # TCONS | XLOC | Reference ID | Transfrag Code | Query ID
    # NA    | NA   | Keep if C=J  | Filter for C=J | Keep if J
    # Reads a .tracking file and extracts IDs that match Transfrag
    # codes c=j. Returns a set of these IDs
    tfCodes = 'c=j'
    ids = set()
    # f = open(filename, 'r')
    with open(filename, 'r') as f:
        content = f.readlines()
    for line in content:
        tokens = line.split("\t")
        tf = tokens[3].lower() # Select the column that is token, make sure is lowercase.
        if tf in tfCodes:
            reference = getTranscriptID(tokens[2])
            query = getTranscriptID(tokens[4])
            ids.add(reference)
            if tf == 'j':
                ids.add(query)
    return ids

def unionTrackingFiles(*args):
    # Since the tracking files themselves are the intersections of two programs,
    # we simply take the UNION of al the .tracking programs
    allIDs = set()
    for filename in args:
        thisIDs = extractIDsFromTrackingFile(filename)
        allIDs.update(thisIDs)
    return allIDs

def makeGtfFromIDs(cellLine, setOfIDs, sourceTools = ["Trinity", "Cufflinks", "Stringtie"]):
    # This step only works if all the original files are named in the following
    # format: CellLine_AssemblyTool_Transcripts.gtf
    # e.g. AV5_N_Cufflinks_Transcripts.tf  D04M_Trinity_Transcripts.gtf
    # Writes the combined .gtf to cellLine_intersected_transcripts.gtf
    nameForGtf = cellLine + "_intersected_transcripts.gtf"
    f = open(nameForGtf, mode = 'w') # Overrites file if file exists.
    cellLine.replace('-', '_')
    cellLine.replace(' ', '_')
    # Walk through all three possible source .gtf files, if they exist
    for tool in sourceTools:
        origGtfName = "%s_%s_Transcripts.gtf" % (cellLine, tool)
        if os.path.isfile(origGtfName):
            with open(origGtfName, mode = 'r') as origGtf:
                content = origGtf.readlines()
            # Walk through each line in each of the original transcript files. If
            # the line's ID matches one of the IDs given, then copy that line
            # into the new output file. This method captures the transcript as
            # well as the exons they contain, becuase we're traversing the
            # original GTF file in order.
            for line in content:
                if len(line) == 0 or line.isspace(): # Skip empty lines
                    continue
                thisID = getTranscriptID(line)
                if thisID is None: # Skip lines that don't contain IDs
                    continue
                if thisID in setOfIDs:
                    f.write(line)
    f.close()

startTime = time.time()
print("Running CuffDiff...")
trackingfiles = runCuffDiff(*sys.argv[1:])
print("Parsing IDs from .tracking files...")
intersection = unionTrackingFiles(*trackingfiles)
print("Making combined .gtf...")
cellLine = getCellLineFromFilename(sys.argv[1])
makeGtfFromIDs(cellLine, intersection)
deltaTime = time.time() - startTime
print("Done in %s seconds" % (deltaTime))
