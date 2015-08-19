helpDoc = """This script runs MuTect with default settings, simplyfing the
inputs for the user. This script takes two arguments, in the following order:
- NORMAL .bam file
- TUMOR .bam file
It automatically the outputfile name as well as the log filename based on
these .bam file inputs. The .bam files must have been processed already by
Picard and splitNCigarReads, which can be run by runPicard.py and 
runSplitNCigarReads.py, respectively.

Written by Kevin Wu, Ortiz Lab UCSF, August 2015
"""

import subprocess
import sys
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

if len(sys.argv) != 3:
    print("Error. Wrong number of arguments.")
    print(helpDoc)
    exit()
# (normalBam, tumorBam, outputFile, logFile)
normalBam = sys.argv[1]
tumorBam = sys.argv[2]

outputFile = "%s_normal_vs_%s_tumor_mutect.out" % (f.getCellLineFromFilename(normalBam), f.getCellLineFromFilename(tumorBam))
logFile = outputFile + ".log"

command = "java -Xmx8g -jar /home/ortiz-lab/software/muTect/mutect-1.1.7.jar --analysis_type MuTect --reference_sequence /media/Data/genomes/hg19_ordered/hg19.fa --cosmic /home/ortiz-lab/software/muTect/bundle/liftedover_output_hg19.vcf --dbsnp /home/ortiz-lab/software/muTect/bundle/dbsnp_138.hg19.excluding_sites_after_129.vcf --input_file:normal %s --input_file:tumor %s --out %s -log %s" % (normalBam, tumorBam, outputFile, logFile)
print(command)
subprocess.call(command, shell = True)
