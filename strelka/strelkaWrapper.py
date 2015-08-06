helpDoc = """This is a wrapper for running the Strelka somatic variant caller. This wrapper
requires the following arguments, in this order:
- .bam file for the tumor
- .bam file for the normal
- Aligner (BWA, ELAND, or Isaac)
Example: python strelkaWrapper.py tumor.bam normal.bam BWA
By default, this wrapper uses the default configuration files provided by
Strelka and runs with 12 threads.

Source:
https://sites.google.com/site/strelkasomaticvariantcaller/home/configuration-and-analysis
Written by Kevin Wu - Ortiz Lab, UCSF - August 2015
"""
# The below is derived from above source.
# example location where strelka was installed to:
# STRELKA_INSTALL_DIR=/opt/strelka_workflow

# example location where analysis will be run:
# WORK_DIR=/data/myWork

# Step 1. Move to working directory:
# cd $WORK_DIR

# Step 2. Copy configuration ini file from default template set to a
#         labsocal copy, possibly edit settings in local copy of file:
# cp $STRELKA_INSTALL_DIR/etc/strelka_config_isaac_default.ini config.ini

# Step 3. Configure:
# $STRELKA_INSTALL_DIR/bin/configureStrelkaWorkflow.pl \
# --normal=/data/normal.bam \
# --tumor=/data/tumor.bam \
# --ref=/data/reference/hg19.fa \
# --config=config.ini --output-dir=./myAnalysis

# Step 4. Run Analysis
#         This example is run using 8 cores on the local host:
# cd ./myAnalysis
# make -j 8

import subprocess
import sys, os

def getCellLineFromFilename(f, delim = "_"):
    splitted = f.split(delim)
    return splitted[0]

def copyDefaultConfigFile(aligner, iniName):
    aligner = aligner.lower() # Converts to lower to avoid case sensitive cases
    fileLocations = {"isaac" : "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin/etc/strelka_config_isaac_default.ini",
                     "eland" : "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin/etc/strelka_config_eland_default.ini",
                     "bwa" : "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin/etc/strelka_config_bwa_default.ini"
    }
    if aligner not in fileLocations:
        print("ERROR: Unrecognized Aligner")
        printHelp()
    fileLoc = fileLocations[aligner]
    copyCommand = "cp %s ./%s" % (fileLoc, iniName)
    # print(copyCommand)
    subprocess.call(copyCommand, shell = True)

def configureStrelka(tumor, normal, configFilename, outputDir):
    configureScript = "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin/bin/configureStrelkaWorkflow.pl"
    args = (configureScript, normal, tumor, configFilename, outputDir)
    command = "%s --tumor=./%s --normal=./%s --ref=/media/Data/genomes/hg19_ordered/hg19.fa --config=./%s --output-dir=./%s" % args
    print("Strelka configuration command:")
    print(command)
    subprocess.call(command, shell = True)

def runStrelka(outputDir):
    # cdCommand = "cd ./%s" % (outputDir)
    # subprocess.call(cdCommand, shell = True)
    # runCommand = "make -j 12" # run with 12 threads by default
    # subprocess.call(runCommand, shell=True)
    command = "make -j 12 -C ./%s" % (outputDir)
    print("Strelka execution command:")
    print(command)
    subprocess.call(command, shell = True)


def parseUserInput(userIn):
    # Input order: tumor, normal, aligner
    # Sanity checks
    if len(userIn) != 4: # Checks for correct number of arguments
        printHelp(True)
    if ".bam" not in userIn[1] or ".bam" not in userIn[2]: # Checks that first two are .bam files
        printHelp(True)
    iniFilename = "%s_tumor_vs_%s_normal_strelka.ini" % (getCellLineFromFilename(userIn[1]), getCellLineFromFilename(userIn[2]))
    outputDir = "%s_tumor_vs_%s_normal_strelka" % (getCellLineFromFilename(userIn[1]), getCellLineFromFilename(userIn[2]))
    copyDefaultConfigFile(userIn[3], iniFilename) # Copys the appropriate ini file given the input aligner
    configureStrelka(userIn[1], userIn[2], iniFilename, outputDir)
    runStrelka(outputDir)

def printHelp(userError = False):
    if userError:
        print("ERROR. Incorrect input parameters.")
    print(helpDoc)
    exit()

# Global variables
strelkaInstallDir = "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin"
currentDir = os.getcwd() # Gets the current directory (still works even when symlinked!)

# Run wrapper
parseUserInput(sys.argv)
