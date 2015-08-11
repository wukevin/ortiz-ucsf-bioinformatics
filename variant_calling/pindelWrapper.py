# http://gmt.genome.wustl.edu/packages/pindel/quick-start.html
# ./pindel -f <reference.fa> -p <pindel_input> [and/or -i bam_configuration_file] -c <chromosome_name> -o <prefix_for_output_files>
import subprocess
import sys
if len(sys.argv) != 3:
    print("Wrapper for pindel. Requires the following inputs, in order:")
    print("- Tumor .bam file")
    print("- Normal .bam file")
    exit()
# Create a bam-configuration file
# Tumor sample
tumorBam = sys.argv[1]
normalBam = sys.argv[2]
if ".bam" not in tumorBam or ".bam" not in normalBam:
    print("Samples must be .bam files.")
    exit()
tumorLine = tumorBam.split("_")[0]
normalLine = normalBam.split("_")[0]
bamConfig = tumorLine + "_vs_" + normalLine + "config.txt"
# Create the bam config file.
bamConfigFile = open(bamConfig, "w")
# The average insert size of 200 was determined from measuring AV1N and AV1P
# using Picard CollectInsertSizeMetrics
bamConfigFile.write(tumorBam + " 200 " + tumorLine + "\n")
bamConfigFile.write(normalBam + " 200 " + normalLine + "\n")
bamConfigFile.close()
outputPrefix = tumorLine + "_vs_" + normalLine + "_pindel"
logFilename = outputPrefix + ".log"
command = "/home/ortiz-lab/software/pindel/pindel/pindel -f /media/Data/genomes/hg19_ordered/hg19.fa -T 8 -i %s -c ALL -o %s | tee %s" % (bamConfig, outputPrefix, logFilename)
print(command)
subprocess.call(command, shell = True)
