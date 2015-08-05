"""


Source:
https://sites.google.com/site/strelkasomaticvariantcaller/home/configuration-and-analysis
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

def parseUserInput(userIn):
    print(userIn)

strelkaInstallDir = "/home/ortiz-lab/software/strelka_workflow-1.0.14/bin"
currentDir = os.getcwd() # Gets the current directory (still works even when symlinked!)

parseUserInput(sys.argv)
