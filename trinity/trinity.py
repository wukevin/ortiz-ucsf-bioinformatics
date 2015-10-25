import os, sys, getopt
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s
import time

helpDoc = """

"""

def executeTrinityGenomeGuided(bamfile):
	#     $TRINITY_HOME/Trinity --genome_guided_bam "$i" --genome_guided_max_intron 11000 --max_memory 54G --CPU 16 --output "$foldername" | tee "$logname"
	outputFolder = bamfile[:-4] + '_trinity_Out'
	logfile = outputFolder + '/trinity.log'
	template = "trinity --genome_guided_bam %s --genome_guided_max_intron 11000 --max_memory 54G --CPU 16 --output %s" % (bamfile, outputFolder)
	s.executeFunctions(template)

def executeTrinityFastq(fastq1, fastq2):
	extracting = False
	# If in gz format, extract such that trintiy can run on it
	if 'gz' in fastq1 and 'gz' in fastq2:
		extracting = True
	if extracting is True:
		f.extractGz([fastq1, fastq2])
		fastq1 = fastq1[:-3]
		fastq2 = fastq2[:-3]
	# Run trinity
	lcs = f.longestCommonSubstring(fastq1, fastq2)
	outputFolder = lcs + '_trinity_Out'
	logfile = outputFolder + '/trinity.log'
	template = 'trinity --left %s --right %s --max_memory 54G --CPU 16 --output %s' % (fastq1, fastq2, outputFolder)
	result = s.executeFunctions(template, captureOutput = True)
	# Write console log to logfile
	f = open(logfile)
	f.write(result)
	f.close()
	# if we extracted earlier, remove the extracted fastq files to save sapce
	if extracting:
		s.executeFunctions('rm ' + fastq1)
		s.executeFunctions('rm ' + fastq2)

def main():
	try:
		optlist, args = getopt.getopt(args = sys.argv[1:], shortopts = None, longopts = ['all-files', 'genome-guided'])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
	runAll = False
	fq = True
	files = []
	# Walk thorugh given options
	for o, a in optlist:
		if o == '--all-files':
			runAll = True
		elif o == '--genome-guided':
			fq = False

	# Caution: this section is not 100% done. Only enough to run what I need right now.
	if runAll is True:
		assert len(args) == 0
		pairs = f.getFastqPairs()
		# Walk through every pair in this dir
		for pair in pairs:
			assert len(pair) == 2
			x, y = None, None
			if "_1" in pair[0]:
				x, y = pair[0], pair[1]
			else:
				x, y = pair[1], pair[0]
			print("Running trinity on %s and %s at %s." % (x, y, time.time()))
			executeTrinityFastq(x,y)	

if __name__ == "__main__":
    main()
