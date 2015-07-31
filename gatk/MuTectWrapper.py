# import os
import subprocess
import sys
if len(sys.argv) != 5:
    print("Error. Wrong number of arguments. Must input four arguments, in this order:")
    print("- Name of normal (not tumor) bam file")
    print("- Name of tumor bam file")
    print("- Name of file to write output")
    print("- Name of file to write log")
    print("This script runs MuTect with default settings, simplifying inputs for user.")
    exit()
# (normalBam, tumorBam, outputFile, logFile)
normalBam = sys.argv[1]
tumorBam = sys.argv[2]
outputFile = sys.argv[3]
logFile = sys.argv[4]
command = "java -Xmx8g -jar /home/ortiz-lab/software/muTect/mutect-1.1.7.jar --analysis_type MuTect --reference_sequence /media/Data/genomes/hg19_ordered/hg19.fa --cosmic /home/ortiz-lab/software/muTect/bundle/liftedover_output_hg19.vcf --dbsnp /home/ortiz-lab/software/muTect/bundle/dbsnp_138.hg19.excluding_sites_after_129.vcf --input_file:normal %s --input_file:tumor %s --out %s -log %s" % (normalBam, tumorBam, outputFile, logFile)
print(command)
subprocess.call(command, shell = True)
