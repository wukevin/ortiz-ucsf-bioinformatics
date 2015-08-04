import subprocess
import sys
import re
import os

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
    # Given a token from a .tracking file, extracts transcript ID
    # Examples
    # Trinity: align_id:160849|GG14081
    # Cufflinks: CUFF.54.1
    # Stringtie: STRG.4.1
    tokens = longstring.split("\t")

    if "CUFF" in longstring:
        match = re.search(r'CUFF\.[0-9]*\.[0-9]*', longstring)
    elif "STRG" in longstring:
        match = re.search(r'STRG\.[0-9]*\.[0-9]*', longstring)
    elif "GG" in longstring and "align_id:" in longstring:
        # Maybe GG is just because Genome-Guided? Maybe not best indentifier
        match = re.search(r'align_id:[0-9]*\|GG[0-9]*',longstring)
    else:
        print("WARNING: Failed to find transcript ID in following token:")
        print(longstring)
        return None
    return match.group(0)

def runCuffDiff(*args):
    commandTemplate = "cuffcompare -s /media/Data/genomes/hg19_ordered/hg19.fa -o %s -r %s %s"
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
        print("python cuffComareAndIntersect AV1_N_Cufflinks_Transcripts.gtf AV1_N_Trinity_Transcripts.gtf")
        exit()
    filename = getCellLineFromFilename(args[0]) + "_cuffcompare_commands.log"
    f = open(filename, mode = "w")
    for command in commands:
        # subprocess.call(command, shell = True)
        print("SKIPPING RUNNING CUFFDIFF FOR FASTER DEBUG")
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
        tf = tokens[3].lower()
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
            for line in content:
                if len(line) == 0 or line.isspace():
                    continue
                thisID = getTranscriptID(line)
                if thisID is None:
                    continue
                if thisID in setOfIDs:
                    # print(thisID)
                    f.write(line)
    f.close()

print("Running CuffDiff...")
trackingfiles = runCuffDiff(*sys.argv[1:])
print("Parsing IDs from .tracking files...")
intersection = unionTrackingFiles(*trackingfiles)
print("Making combined .gtf...")
cellLine = getCellLineFromFilename(sys.argv[1])
makeGtfFromIDs(cellLine, intersection)
print("Done")
