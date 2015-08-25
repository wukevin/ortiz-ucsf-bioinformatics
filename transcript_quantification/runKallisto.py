helpDoc = """This is a wrapper for kallisto that simply automatically generates the
output directory based on the input fastq filenames. Also automatically runs 10
bootsrap samples. Must have the following arguments in order:
- fastq1
- fastq2
- Kallisto index to quantify
Optionally, you can specificy that we should manually determine the average fastq
fragment length because kallisto's determination doesn't work sometimes. This is
done by using the --manualLength flag
Example usage: python runKallisto.py [--manualLength] x_1.fastq x_2.fastq abc.kindex

Kevin Wu - Ortiz Lab UCSF - August 2015"""

import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s
import re

from multiprocessing import Pool as ThreadPool

def runKallisto(fastq1, fastq2, index):
	commandTemplate = "kallisto quant --index=%s --output-dir=%s --bootstrap-samples=10 --threads=10 %s %s"
	common = f.longestCommonSubstring(fastq1, fastq2)
	command = commandTemplate % (index, common, fastq1, fastq2)
	s.executeFunctions(command)

def runKallistoManualLength(fastq1, fastq2, index):
	print("Reading average read length for fastq files...")
	pool = ThreadPool(2)
	results = pool.map(f.meanFastqReadLength, [fastq1, fastq2])
	# length1 = f.meanFastqReadLength(fastq1)
	# length2 = f.meanFastqReadLength(fastq2)
	# if length1 != length2:
	# 	print("WARNING: Two fastq's length are different")
	# length = (length1 + length2) / 2
	if results[0] != results [1]:
		print("WARNING: Two fastq's length are different")
	length = sum(results) / 2
	print("Average fragment length is " + str(length))
	commandTemplate = "kallisto quant -l %s --index=%s --output-dir=%s --bootstrap-samples=10 --threads=10 %s %s"
	common = f.longestCommonSubstring(f.stripKnownFileExtensions(fastq1), f.stripKnownFileExtensions(fastq2))
	command = commandTemplate % (length, index, common, fastq1, fastq2)
	print(command)
	s.executeFunctions(command)

def parseUserInput(args):
	if len(args) < 3 or len(args) > 4:
		print("Incorrect number of arguments.")
		print(helpDoc)
	elif len(args) == 3:
		runKallisto(args[0], args[1], args[2])
	elif len(args) == 4 and args[0] == "--manualLength":
		runKallistoManualLength(args[1], args[2], args[3])
	else: 
		print("Unrecognized arguments.")
		print(helpDoc)

parseUserInput(sys.argv[1:])