import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s
import re
import numpy as np

from multiprocessing import Pool as ThreadPool

helpDoc = """Wrapper to run HTSeq. Use the following commands:
ls *.bam | python htseq.py --referenceGtf xxx.gtf
OR
python htseq.py --referenceGtf xxx.gtf yyy.bam

Written by Kevin Wu - Ortiz Lab - October 2015"""

def htseqWrapper(bamfile, refGtf):
	# htseq-count --format=bam --stranded=no [STAR Bam File] [Reference.gtf] > [OutputName.txt]
	outName = f.stripKnownFileExtensions(bamfile) + ".htseq-count.txt"
	command = "htseq-count --format=bam --stranded=no %s %s > %s" % (bamfile, refGtf, outName)
	results = s.executeFunctions(outName, captureOutput = True)
	logName = f.stripKnownFileExtensions(bamfile) + ".htseq-count.log"
	# Write to log file
	f = open(logName, mode = 'w')
	f.write(results)
	f.close()

def htseqOneArg(tupleOfArgs):
	htseqWrapper(tupleOfArgs[0], tupleOfArgs[1])

def htseqParallel(listOfBams, referenceGtf, threadCount = 4):
	pool = ThreadPool(threadCount)
	inputArgsList = []
	for bam in listOfBams:
		inputArgsList.append([bam, referenceGtf])
	pool.map(htseqOneArg, inputArgsList)

arguments = sys.argv[1:]

if s.isStdInEmpty():
	# Process command line args
	if len(arguments) != 3:
		print("Incorrect number of arguments")
		print(helpDoc)
	else:
		if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1] and 'bam' in arguments[2]:
			htseqWrapper(arguments[1], arguments[2])
		else:
			print("Wrong arguments")
			print(helpDoc)
else:
	STDIN = s.getStdIn()
	if arguments[0] == "--referenceGtf" and gtf in arguments[1]:
		htseqParallel(STDIN, arguments[1])
	else:
		print("Incorrect usage.")
		print(helpDoc)
