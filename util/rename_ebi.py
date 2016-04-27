import sys, os
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
import shellUtil as s
import glob
import getopt

def getMapDict(file = "/media/rawData/Ortiz_EBI_Download/EBI_Sample_Map.txt"):
	mapFile = open(file, 'r')
	mapDict = {}
	for line in mapFile:
		if "Sample" in line and "Cell_Line" in line:
			continue
		splitted = line.rstrip().split('\t')
		mapDict[splitted[0]] = splitted[1]
	return mapDict

def fileRename(suffix, dict, simulate = True):
	logfile = open('rename.mapping', 'w')
	for key in dict:
		value = dict[key]
		matches = glob.glob('*' + key + suffix)
		assert len(matches) == 1
		originalFilename = matches[0]
		newFilename = value + suffix
		logfile.write(originalFilename + '\t' + newFilename + '\n')
		if simulate:
			continue
		os.rename(originalFilename, newFilename)
	logfile.close()

def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts = None, longopts = ['suffix=', 'simulate'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    suffix = '.bam'
    simulate = False
    for o, a in optlist:
        # print(o)
        if o == '--suffix':
            suffix = a
        elif o == '--simulate':
            simulate = True
        else:
            print("Unrecognized option: " + o)
            sys.exit(2)
    dict = getMapDict()
    fileRename(suffix, dict, simulate)


if __name__ == '__main__':
    main()