helpDoc = """This is a wrapper to run STAR. It takes in the following arguments:
- fastq1 - the forward read fastq
- fastq2 - the reverse read fastq
Order of these is important!

We output a .bam file that is sorted by coordinate. We also use STAR flags that
make the output compatible with the Cuff suite of tools. 

By default, we run without generating a custom genome indices. Genrating custom
indices increases accuracy at the cost of significantly longer computation times.
However, you can enable such functionality by using the flag --generate-genome. 
Using this flag after already having run STAR once will RERUN STAR from the
beginning.

Example usage:
python runSTAR.py [--generate-genome] x.fastq y.fastq

Kevin Wu - Ortiz Lab UCSF - August 2015"""

# Model:
# STAR --outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical --outSAMtype BAM SortedByCoordinate --genomeDir /media/Data/genomes/STAR_index_hg19_vGATK/STAR_genomeDir_hg19_vGATK --readFilesIn $Forward $Reverse --runThreadN 16

import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

def runStar(fastq1, fastq2, genome = "/media/Data/genomes/STAR_index_hg19_vGATK/STAR_genomeDir_hg19_vGATK"):
	# Runs STAR to output a coordinate soorted BAM file that is compatible with cuff
	lcs = f.longestCommonSubstring(fastq1, fastq2) # lcs = longest common substring
	commandTemplate = "STAR --outSAMstrandField intronMotif --outFilterIntronMotifs RemoveNoncanonical --outSAMtype BAM SortedByCoordinate --genomeDir %s --readFilesIn %s %s --runThreadN 16 --outFileNamePrefix %s"
	if "gz" in fastq1 and "gz" in fastq2:
		commandTemplate = commandTemplate + " --readFilesCommand zcat"
	command = commandTemplate % (genome, fastq1, fastq2, lcs)
	print(command)
	s.executeFunctions(command)

def runStarGenome(fastq1, fastq2):
	# STAR --runMode genomeGenerate --genomeDir $genomeDir2 --genomeFastaFiles $hg19dir --sjdbFileChrStartEnd $runDir/SJ.out.tab --sjdbOverhang 75 --runThreadN 16
	genomeDir = f.longestCommonSubstring(fastq1, fastq2) + "_genome_generation"
	s.executeFunctions("mkdir " + genomeDir) # Make the directory, so we can output to it.
	inputSJ = f.longestCommonSubstring(fastq1, fastq2) + "_SJ.out.tab"
	commandTemplate = "STAR --runMode genomeGenerate --genomeDir %s --genomeFastaFiles /media/Data/genomes/GATK_hg19/hg19/ucsc.hg19.fasta --sjdbFileChrStartEnd %s --sjdbOverhang 75 --runThreadN 16"
	if "gz" in fastq1 and "gz" in fastq2:
		commandTemplate = commandTemplate + " --readFilesCommand zcat"
	command = commandTemplate % (genomeDir, inputSJ)
	return genomeDir # Return the directory the genome was written to so we can use in subsequent star run.

def parseUserInput(args):
	# Sanity check.
	if len(args) > 3 or len(args) < 2:
		print("Too few args")
		print(helpDoc)
	# Done with sanity check
	elif len(args) == 2:
		runStar(args[0], args[1])
	elif args[0] == "--generate-genome":
		runStar(args[1], args[2]) # Runs star once, get the SJ.out.tab file
		gDir = runStarGenome(args[1], args[2]) # Runs the genome generatino using above output.
		runStar(args[1], args[2], gDir) # Runs STAR again using custom genome.
	else:
		print("Unrecognized arguments.")
		print(helpDoc)


parseUserInput(sys.argv[1:])

