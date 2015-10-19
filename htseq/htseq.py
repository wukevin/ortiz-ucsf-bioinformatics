import sys, subprocess, os
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

Note that HTSeq requires input BAM files to be sorted by NAME. If running on
STAR's output, and the output is already sorted by STAR, we do not need to
further sort it.
Written by Kevin Wu - Ortiz Lab - October 2015"""

def htseqWrapper(bamfile, refGtf):
	# htseq-count --format=bam --stranded=no [STAR Bam File] [Reference.gtf] > [OutputName.txt]
	outName = f.stripKnownFileExtensions(bamfile) + ".htseq-count.txt"
	if os.path.isfile(outName): # If the output txt already exists, don't recompute it
		return None
	command = "htseq-count --format=bam --stranded=no %s %s > %s" % (bamfile, refGtf, outName)
	results = s.executeFunctions(command)
	# logName = f.stripKnownFileExtensions(bamfile) + ".htseq-count.log"
	# Write to log file
	# logFile = open(logName, mode = 'w')
	# logFile.write(results)
	# logFile.close()

def htseqOneArg(tupleOfArgs):
	htseqWrapper(tupleOfArgs[0], tupleOfArgs[1])

def htseqParallel(listOfBams, referenceGtf, threadCount = 4):
	pool = ThreadPool(threadCount)
	inputArgsList = []
	for bam in listOfBams:
		inputArgsList.append([bam, referenceGtf])
	pool.map(htseqOneArg, inputArgsList)

def readHtseqCountResult(file):
	"""Returns a dictionary where keys are genes, values are counts in that result"""
	output = {}
	f = open(file)
	if ".htseq-count.txt" not in file:
		print("WARNING: The file supplied may not be a htseq count result file")
	for line in f:
		if line.startswith("_"):
			continue
		splitted = line.split('\t')
		output[splitted[0]] = int(splitted[1])
	f.close()
	return output

def aggregateHtseqCountResults(listOfResultFiles, tableOutFile = 'aggregated_htseq_table.csv', sumamryOutFile = 'aggregated_htseq_summary.csv'):
	# pool = ThreadPool(4)
	# listOfDict = pool.map(readHtseqCountResult, listOfResultFiles)
	print("Reading in results")
	allResults = {} # Dict of dicts. First index by filename, then by gene
	for result in listOfResultFiles:
		allResults[result] = readHtseqCountResult(result)
	allGenes = [x for x in allResults[listOfResultFiles[0]]]
	table = {} # Each entry in this dict is a gene, followed by a list of values
	for gene in allGenes: # initialize the table
		table[gene] = []
	print("Aggregating results")
	for gene in allGenes:
		# print("Aggregating counts for %s" % (gene))
		for result in listOfResultFiles:
			resultDict = allResults[result]
			try:
				thisGeneVal = int(resultDict[gene])
			except KeyError:
				print("Caution: %s not found in result file %s" % (gene, result))
				thisGeneVal = -1
			table[gene].append(thisGeneVal)
		assert len(table[gene]) == len(listOfResultFiles)
	x = open(tableOutFile, 'w')
	header = 'genes,' + ','.join(listOfResultFiles) + "\n"
	x.write(header)
	for gene in allGenes:
		stringified = [str(g) for g in table[gene]]
		dataInCsv = ','.join(stringified)
		lineToWrite = gene + ',' + dataInCsv + "\n"
		x.write(lineToWrite)
	x.close()
	print("Computing summary statistics")
	y = open(sumamryOutFile, 'w')
	header = 'genes,mean,sd,median,max,min,numMissingValues\n'
	y.write(header)
	for gene in allGenes:
		# data = [allResults[x][gene] for x in listOfResultFiles]
		data = table[gene]
		ogLength = len(data)
		data = [x for x in data if x > -1] # Filter out -1 values
		numMissing = len(data) - ogLength
		avg = np.mean(data)
		std = np.std(data)
		med = np.median(data)
		lineToWrite = "%s,%s,%s,%s,%s,%s,%s\n" % (gene, avg, std, med, max(data), min(data), numMissing)
		y.write(lineToWrite)
	y.close()

# arguments = sys.argv[1:]

# if s.isStdInEmpty():
# 	# Process command line args
# 	if len(arguments) != 3:
# 		print("Incorrect number of arguments")
# 		print(helpDoc)
# 	else:
# 		if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1] and 'bam' in arguments[2]:
# 			htseqWrapper(arguments[2], arguments[1])
# 		else:
# 			print("Wrong arguments")
# 			print(helpDoc)
# else:
# 	STDIN = s.getStdIn()
# 	if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1]:
# 		htseqParallel(STDIN, arguments[1])
# 	else:
# 		print("Incorrect usage.")
# 		print(helpDoc)
