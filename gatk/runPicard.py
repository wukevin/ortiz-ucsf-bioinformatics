import os
import subprocess
# Creates bash script to run Picard on all STAR .bam files in the current
# directory. Then runs SplitNCigarReads on each of those outputs as well. After
# running resultant script, everything should be ready for variant calling.
# Source: https://www.broadinstitute.org/gatk/guide/topic?name=methods
dirFiles = os.listdir(os.getcwd())
outputScript = open("runPicard.bash", "w")
outputScript.write("#!/bin/bash\n")
for f in dirFiles:
  if os.path.isfile(os.path.join(os.getcwd(),f)) and ".sortedByCoord.out.bam" in f:
    bamFile = f
    cellLine = bamFile.split("_")[0]
    # Runs AddOrReplaceReadGroups
    command = "java -Xmx8g -jar ~/software/picard/picard/dist/picard.jar AddOrReplaceReadGroups I="
    command = command + bamFile + " "
    command = command + "O=" + cellLine + "_rg_added_sorted.bam "
    command = command + "SO=coordinate RGID=1 RGLB=illumina RGPL=illumina RGPU=illumina RGSM=" + cellLine + "\n"
    outputScript.write(command)
    # Runs MarkDuplicates
    command = "java -Xmx8g -jar ~/software/picard/picard/dist/picard.jar MarkDuplicates I=" + cellLine + "_rg_added_sorted.bam "
    command = command + "O=" + cellLine + "_dedupped.bam "
    command = command + "CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=" + cellLine + "output.metrics\n"
    outputScript.write(command)
    outputScript.write("\n")
outputScript.close()
print("Now run the script runPicard.bash. Make sure to chmod it first.")
# java -Xmx2g -jar ~/software/picard/picard/dist/picard.jar AddOrReplaceReadGroups I=D04M_Aligned.sortedByCoord.out.bam O=D04M_rg_added_sorted.bam RGID=1 RGLB=illumina RGPL=illumina RGPU=illumina RGSM=D04M
