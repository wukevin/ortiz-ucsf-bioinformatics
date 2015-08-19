helpDoc = """Runs Picard on all STAR .bam files in the current directory. It does this
using one thread per .bam file by default because AddOrReplaceReadGroups
and MarkDuplicates are single threaded, and running all samples in parallel
decreases runtime without putting too much strain on I/O.

This can be run in two different ways 

Author: Kevin Wu, Ortiz Lab UCSF, August 2015
Source: https://www.broadinstitute.org/gatk/guide/topic?name=methods"""
import os, sys
import subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil
import shellUtil as s

def runPicard(listOfBams):
    readGroupsCommands = []
    markDuplicatesCommands = []
    for bamFile in listOfBams:
        cellLine = fileUtil.getCellLineFromFilename(bamFile)
        # Runs AddOrReplaceReadGroups
        # Template: java -Xmx8g -jar ~/software/picard/picard/dist/picard.jar AddOrReplaceReadGroups I=star_output.sam O=rg_added_sorted.bam SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample
        commandTemplate = "java -Xmx8g -jar ~/software/picard/picard/dist/picard.jar AddOrReplaceReadGroups I=%s O=%s_rg_added_sorted.bam SO=coordinate RGID=1 RGLB=illumina RGPL=illumina RGPU=illumina RGSM=%s"
        command = commandTemplate % (bamFile, cellLine, cellLine)
        readGroupsCommands.append(command)
        # command = command + bamFile + " "
        # command = command + "O=" + cellLine + "_rg_added_sorted.bam "
        # command = command + "SO=coordinate RGID=1 RGLB=illumina RGPL=illumina RGPU=illumina RGSM=" + cellLine + "\n"
        # outputScript.write(command)
        # Runs MarkDuplicates
        # Template: java -jar MarkDuplicates I=rg_added_sorted.bam O=dedupped.bam  CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=output.metrics 
        commandTemplate = "java -Xmx8g -jar ~/software/picard/picard/dist/picard.jar MarkDuplicates I=%s_rg_added_sorted.bam O=%s_dedupped.bam CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=%s_dedupped.metrics"
        command = commandTemplate % (cellLine, cellLine, cellLine)
        markDuplicatesCommands.append(command)
        # command = command + "O=" + cellLine + "_dedupped.bam "
        # command = command + "CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=" + cellLine + "output.metrics\n"
        # outputScript.write(command)
        # outputScript.write("\n")
    s.executeFunctions(readGroupsCommands, parallel = True, simulate = True)
    s.executeFunctions(markDuplicatesCommands, parallel = True, simulate = True)

if s.isStdInEmpty():
    if len(sys.argv) > 1:
        runPicard(sys.argv[1:])
    else:
        print("Error. No piped input or command line arguments")
        print(helpDoc)
else:
    runPicard(s.getStdIn())
