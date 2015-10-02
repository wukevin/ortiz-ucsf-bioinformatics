import re
import glob

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
