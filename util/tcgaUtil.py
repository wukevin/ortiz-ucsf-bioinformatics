import sys, subprocess, glob, os
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
import shellUtil as s
import re

def getPrefixForIDs(ids, idmapfile = '/media/rawData/TCGA_SKCM/ids_to_filename.txt'):
	idDict = dict()
	idmap = open(idmapfile, mode = 'r')
	for line in idmap:
		parsed = line.split()
		idDict[parsed[0]] = parsed[1]
		# Stored as TCGA-XX-XXXX filenameprefix
	if isinstance(ids, str):
		ids = ids.split()
	prefixes = []
	# print(ids)
	for i in ids:
		# print(i)
		prefixes.append(idDict[i])
	return prefixes

def getSequenceFilenameFromTCGABarcode(tcgaID, disease_abbr):
	# command = 'cgquery "disease_abbr=%s&refassem_short_name=unaligned&library_strategy=RNA-Seq&legacy_sample_id=%s-*" | grep filename' % (disease_abbr, tcgaID)
	def _padToThreeAddL(num):
		num = num[0]
		x = str(num)
		while len(x) < 3:
			x = '0' + x
		x = 'L' + x
		return x
	command = 'cgquery "disease_abbr=%s&refassem_short_name=unaligned&library_strategy=RNA-Seq&legacy_sample_id=%s-*"' % (disease_abbr, tcgaID)
	output = s.executeFunctions(command, captureOutput = True)
	lines = output.split('\n')
	for line in lines:
		if 'filename' in line:
			x = line.split('.')[2]
			tokens = x.split('_')
			tokensFiltered = [i for i in tokens if len(i) > 1]
			weirdNumber = [i for i in tokens if len(i) == 1]
			tokensFiltered.append(_padToThreeAddL(weirdNumber))
			joined = '_'.join(tokensFiltered)
			return joined

def queryAndDownload(queryString, keyfile, download = False):
    queryCommand = 'cgquery -o temp.xml "%s"' % (queryString)
    s.executeFunctions(queryCommand)
    if download:
	    downloadCommand = 'gtdownload -vv -c %s -d temp.xml' % (keyfile)
	    s.executeFunctions(downloadCommand)

def getAnalysisIDs(participant_id): 
    commandTemplate = 'cgquery "participant_id=%s&library_strategy=RNA-Seq"'
    command = commandTemplate % (participant_id)
    print(command)
    output = subprocess.check_output(command, shell = True).splitlines()
    ids = []
    for line in output:
        if "analysis_id" in line:
            tokens = line.split(":")
            tokens = [x.strip() for x in tokens]
            ids.append(tokens[1])
    return ids

def getMetadataFromSequenceFilename(filename, metadataTag):
	# Only supports from .bam or .fastq.gz or derivatives
	# 140624_UNC15-SN850_0372_AC4L6NACXX_ACTGAT_L007_Aligned.sortedByCoord.out
	# print(getMetadataFromSequenceFilename('140624_UNC15-SN850_0372_AC4L6NACXX_ACTGAT_L007_Aligned.sortedByCoord.out.bam', 'UVM', 'legacy_sample_id'))
	print("Fetching metadata tag %s for: %s" % (metadataTag, filename))
	filename = filename.split('.')[0]
	tokens = filename.split('_')
	tokens = tokens[:6]
	weirdNumberToken = [x for x in tokens if 'L' in x and len(x) == 4]
	tokens.remove(weirdNumberToken[0])
	weirdNumber = int(weirdNumberToken[0][1:])
	tokens.insert(4, str(weirdNumber))
	reconstructed = '_'.join(tokens)
	# print(reconstructed)
	# queryString = 'cgquery "disease_abbr=%s&refassem_short_name=unaligned&library_strategy=RNA-Seq&filename=*%s*"' % (disease_abbr, reconstructed)
	queryString = 'cgquery "refassem_short_name=unaligned&library_strategy=RNA-Seq&filename=*%s*"' % (reconstructed)
	output = s.executeFunctions(queryString, captureOutput = True)
	# print(output)
	lines = output.split('\n')
	for line in lines:
		if "downloadable_file_count" in line:
			num = int(line.split(':')[1])
			if num != 1:
				return "ERROR"
	for line in lines:
		if metadataTag in line:
			return line.split(':')[1].strip()
	return "ERROR"

# print(getMetadataFromSequenceFilename('140624_UNC15-SN850_0372_AC4L6NACXX_ACTGAT_L007_Aligned.sortedByCoord.out.bam', 'legacy_sample_id'))
