helpDoc = """This is a wrapper to run STAR. It takes in the following arguments:
- fastq1 - the forward read fastq
- fastq2 - the reverse read fastq (This specific order!)
By default, we run without generating a custom genome indices. This increases
accuracy at the cost of significantly longer computation times. However, we can
enable such functionality by using the flag --generate-genome. Example usage:
python runSTAR.py [--generate-genome] x.fastq y.fastq

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
	lcs = f.longestCommonSubstring(fastq1, fastq2)
	commandTemplate = "STAR --outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical --outSAMtype BAM SortedByCoordinate --genomeDir %s --readFilesIn %s %s --runThreadN 16 --outFileNamePrefix %s"
	command = commandTemplate % (genome, fastq1, fastq2, lcs)
	s.executeFunctions(command)

def runStarGenome(fastq1, fastq2):
	# STAR --runMode genomeGenerate --genomeDir $genomeDir2 --genomeFastaFiles $hg19dir --sjdbFileChrStartEnd $runDir/SJ.out.tab --sjdbOverhang 75 --runThreadN 16
	genomeDir = "genome_generation"
	s.executeFunctions("mkdir " + genomeDir)
	inputSJ = f.longestCommonSubstring(fastq1, fastq2) + "_SJ.out.tab"
	commandTemplate = "STAR --runMode genomeGenerate --genomeDir %s --genomeFastaFiles /media/Data/genomes/GATK_hg19/hg19/ucsc.hg19.fasta --sjdbFileChrStartEnd %s --sjdbOverhang 75 --runThreadN 16"
	command = commandTemplate % (genomeDir, inputSJ)

def parseUserInput(args):
	if len(args) > 3 or len(args) < 2:
		print("Too few args")
		print(helpDoc)
		exit()
	# Done with sanity check
	if len(args) == 2:
		runStar(args[0], args[1])
	elif args[0] == "--generate-genome":
		runStar(args[0], args[1])
		runStarGenome(args[0], args[1])
		runStar(args[0], args[1], "genome_generation")
		exit()


parseUserInput(sys.argv[1:])

