"""
Utility functions for working with FASTA files. Includes various functions for 
reading and writing FASTA files.

Written by Kevin Wu in Ortiz Lab, May 2015
"""

import genomeUtil as g

def writeFASTA(filename, header, sequence, trimHeaders = True, append = True):
    # Allows us to deal with both file inputs and strings as input.
    if type(filename) == file:
    	fileOut = filename
    	if append == True:
    		fileOut = open(fileOut.name, mode = "a")
    	else:
    		fileOut = open(fileOut.name, mode = "w")
    else:
	    if append == True:
	        fileOut = open(filename, mode = "a")
	    else:
	        fileOut = open(filename, mode = "w")
    sequenceSplitted = g.splitSequence(sequence, 80)
    if trimHeaders == True:
    	header = truncateFASTAHeader(header)
    fileOut.write(header + "\n")
    for seq in sequenceSplitted:
        fileOut.write(seq + "\n")
    fileOut.write("\n")
    fileOut.close()

def readFASTA(filename):
	# Allows us to deal with both file objects and with strings as input
	if type(filename) == file:
		inFile = filename
	else:
		inFile = open(filename, 'r')
	content = inFile.readlines()
	inFile.close()
	fastaDict = {} # Stores fasta sequences. Key is header, entry is fasta sequence
	for line in content:
		line = line.rstrip('\n') # Remove newlines
		if ">" in line:
			fastaDict[line] = ""
			latestHeader = line
		else:
			fastaDict[latestHeader] = fastaDict[latestHeader] + line
	return fastaDict


def splitSequence(line, n = 1):
    """
    Splits a nucelotide sequence into units of length n.
    """
    splitted = [line[i:i+n] for i in range(0, len(line), n)]
    return splitted

def truncateFASTAHeader(fastaHeader, length = 80):
	splilitedHeader = splitSequence(fastaHeader, length)
	header = splitted[1]
	return header
