import os
import subprocess
# Runs SplitNCigarReads on each of the outputs of runPicard.bash. After
# running resultant script, everything should be ready for variant calling.
# Source: https://www.broadinstitute.org/gatk/guide/topic?name=methods
outputScript = open("runSplitNCigarReads.bash", "w")
outputScript.write("#!/bin/bash\n")
dirFiles = os.listdir(os.getcwd())
for f in dirFiles:
  if os.path.isfile(os.path.join(os.getcwd(),f)) and "_dedupped.bam" in f:
      bamFile = f
      cellLine = bamFile.split("_")[0]
      command = "java -Xmx8g -jar /home/ortiz-lab/software/GenomeAnalysisTK-3.4-46/GenomeAnalysisTK.jar -T SplitNCigarReads -R /media/Data/genomes/hg19_ordered/hg19.fa -I "
      command = command + bamFile + " -o " + cellLine + "_split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS\n"
      outputScript.write(command)
outputScript.close()
print("Commands written to runSplitNCigarReads.bash.")

# java -jar GenomeAnalysisTK.jar -T SplitNCigarReads -R ref.fasta -I dedupped.bam -o split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS
# /home/ortiz-lab/software/GenomeAnalysisTK-3.4-46/GenomeAnalysisTK.jar
