import sys
import subprocess

doc = """This is a wrapper for Pindel's built-in filtering mechanism. It takes
only one argument, the pindel run to filter. For example, Pindel outputs a set
of files that end in xxx_D, xxx_INV, and so on, then you would run:
python pindelIndelFilter.py xxx

Written by Kevin Wu, Ortiz Lab UCSF, August 2015
"""

def configureConfig(inputFile, outputFile, configFileName):
    configLines = ["indel.filter.input = %s\n",
                   "indel.filter.vaf = 0.08\n",
                   "indel.filter.cov = 20\n",
                   "indel.filter.hom = 6\n",
                   "indel.filter.pindel2vcf = /home/ortiz-lab/software/pindel/pindel/pindel2vcf\n",
                   "indel.filter.reference = /media/Data/genomes/hg19_ordered/hg19.fa\n",
                   "indel.filter.referencename = hg19.fa\n",
                   "indel.filter.referencedate = 022009\n",
                   "indel.filter.output = %s\n"]
    configLines[0] = configLines[0] % inputFile
    configLines[8] = configLines[8] % outputFile
    f = open(configFileName, mode = "w")
    # Write our custom config file.
    for line in configLines:
        f.write(line)
    f.close()
    print("Wrote config file " + configFileName)

def grepToHeads(pindelRunName):
    print("Consolidating headers using following command:")
    command = "grep ChrID %s* > %s_all.head" % (pindelRunName, pindelRunName)
    print(command)
    subprocess.call(command, shell = True)
    tokenziedCommand = command.split(" ")
    headFileName = tokenziedCommand[len(tokenziedCommand) - 1]
    print("Consolidated headers to " + headFileName)
    return headFileName

def parseUserInput(pindelRunName):
    headFileName = grepToHeads(pindelRunName)
    outfile = headFileName + ".filter.output"
    configFilename = headFileName + ".filter.config"
    logfile = headFileName + ".filter.log"
    configureConfig(headFileName, outfile, configFilename)
    execCommand = "perl /home/ortiz-lab/software/pindel/pindel/somatic_filter/somatic_indelfilter.pl %s | tee %s" % (configFilename, logfile)
    print("Executing filtering with following command:")
    print(execCommand)
    subprocess.call(execCommand, shell = True)

if len(sys.argv) == 2:
    parseUserInput(sys.argv[1])
else:
    print(doc)
    exit()
