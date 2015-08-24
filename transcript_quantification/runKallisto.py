helpDoc = """This is a wrapper for kallisto that simply automatically generates the
output directory based on the input fastq filenames. Also automatically runs 10
bootsrap samples. Must have the following arguments in order:
- fastq1
- fastq2
- Kallisto index to quantify

Kevin Wu - Ortiz Lab UCSF - August 2015"""

import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

def runKallisto(fastq1, fastq2, index):
	commandTemplate = "kallisto quant --index=%s --output-dir=%s --bootstrap-samples=10 --threads=10 %s %s"
	common = f.longestCommonSubstring(fastq1, fastq2)
	command = commandTemplate % (index, common, fastq1, fastq2)
	s.executeFunctions(command)

def parseUserInput(args):
	if len(args) != 3:
		print("Incorrect number of arguments.")
		print(helpDoc)
	else:
		runKallisto(args[0], args[1], args[2])

parseUserInput(sys.argv[1:])