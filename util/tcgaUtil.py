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

def getSequenceFilenameFromTCGAID(tcgaID, disease_abbr):
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

print(getSequenceFilenameFromTCGAID('TCGA-D3-A3CE', 'SKCM'))