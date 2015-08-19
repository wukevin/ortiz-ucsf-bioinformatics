helpDoc = """This is a wrapper to run STAR. It takes in the following arguments:
- fastq1 - the forward read fastq
- fastq2 - the reverse read fastq
By default, we run without generating a custom genome indices. This increases
accuracy at the cost of significantly longer computation times. However, we can
enable such functionality by using the flag --genomeGenerate. Example usage:
python runSTAR.py [--genomeGenerate] x.fastq y.fastq

Kevin Wu - Ortiz Lab UCSF - August 2015"""

# Model:
# STAR --outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical --outSAMtype BAM SortedByCoordinate --genomeDir /media/Data/genomes/STAR_index_hg19_vGATK/STAR_genomeDir_hg19_vGATK --readFilesIn $Forward $Reverse --runThreadN 16

import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

# print(f.longestCommonSubstring("Hello t here", "Hello there"))

def runStar(fastq1, fastq2, genome = "/media/Data/genomes/STAR_index_hg19_vGATK/STAR_genomeDir_hg19_vGATK"):
	# Runs STAR to output a coordinate soorted BAM file that is compatible with cuff
	commandTemplate = "STAR --outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical --outSAMtype BAM SortedByCoordinate --genomeDir %s --readFilesIn %s %s --runThreadN 16"
	command = commandTemplate % (genome, fastq1, fastq2)
	s.executeFunctions(command)

def generateGenome(): 
	return None

def parseUserInput(args):
	# if len(args) > 3 or len(args) < 2:
	# 	print("Too few args")
	# 	print(helpDoc)
	# print(args)
	runStar(args[0], args[1])

parseUserInput(sys.argv[1:])

