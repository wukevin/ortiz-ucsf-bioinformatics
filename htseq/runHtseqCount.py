import sys, os
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/htseq/")
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import htseq as h

arguments = sys.argv[1:]

if s.isStdInEmpty():
	# Process command line args
	if len(arguments) != 3:
		print("Incorrect number of arguments")
		print(helpDoc)
	else:
		if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1] and 'bam' in arguments[2]:
			h.htseqWrapper(arguments[2], arguments[1])
		else:
			print("Wrong arguments")
			print(helpDoc)
else:
	STDIN = s.getStdIn()
	if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1]:
		h.htseqParallel(STDIN, arguments[1], threadCount = 16)
	else:
		print("Incorrect usage.")
		print(helpDoc)