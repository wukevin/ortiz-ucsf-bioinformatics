import re
import glob

def getPrefixForIDs(ids, idmapfile = '/media/rawData/TCGA_SKCM/ids_to_filename.txt'):
	idDict = dict()
	idmap = open(idmapfile, mode = 'r')
	for line in idmap:
		parsed = l.split()
		idDict[parsed[0]] = parsed[1]
		# Stored as TCGA-XX-XXXX filenameprefix
	idsList = ids.split()
	prefixes = []
	for i in idsList:
		prefixes.append(idDict[i])
	return prefixes
