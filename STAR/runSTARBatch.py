#!/usr/bin/python
helpDoc = """Symlink this file to whatever directory your fastq.gz files are in, and run it to 
generate STAR .bam files for every fastq pair you have.
"""
import sys, subprocess, os, glob, re
sys.path.append(os.environ['PIPELINEHOME'] + "/STAR/")
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
import fileUtil as f
import shellUtil as s
import star
import os.path

from multiprocessing import Pool as ThreadPool

# k.runKallistoManualLength()
numthreads = max(s.getAvailableThreads(), 12)
# pwd = os.getcwd()
# listOfPrefixes = glob.glob("*_1.fastq.gz") # Get all unique fastq pairs in current folder
# listOfPrefixes= [re.sub('_1.fastq.gz', '', x) for x in listOfPrefixes] # Remove the last bit
# # listOfPrefixes = listOfPrefixes[427:]
# # print(len(listOfPrefixes))
# for i in listOfPrefixes:# If already exists a bam, then don't redo it.
#     fname = i + "_Aligned.sortedByCoord.out.bam"
#     if os.path.isfile(fname):
#         listOfPrefixes = [x for x in listOfPrefixes if x != i]
# print(len(listOfPrefixes))
fastqGzFiles = glob.glob("*.fastq.gz")
fastqGzPairs = f.pairGivenFastqFiles(fastqGzFiles)

# pairFiles = []
# singleFiles = []
# for x in listOfPrefixes:
#     if os.path.isfile(x + "_2.fastq"):
#         pairFiles.append((x + "_1.fastq", x + "_2.fastq"))
#     else:
#         singleFiles.append(x + "_1.fastq")
# listOfFiles = [(x + "_1.fastq", x + "_2.fastq") for x in listOfPrefixes]

import time

def runStarPairWrap(tupleOfFiles):
    print("\n\n")
    startTime = time.time()
    # print("Starting STAR run on " + str(tupleOfFiles))
    result = star.runStar(tupleOfFiles[0], tupleOfFiles[1], "/media/rawData/genomes/STAR_genomeDir_hg19_vGATK", cpu = numthreads)
    logfile = open(lcs(tupleOfFiles[0], tupleOfFiles[1]), 'w')
    logfile.write(result)
    logfile.close()
    # k.runKallistoManualLength(tupleOfFiles[0], tupleOfFiles[1], "/media/Data2/TCGA_SKCM/raw_data/MIRAT.kindex")
    # command = "python runSTAR.py %s %s %s" % (tupleOfFiles[0], tupleOfFiles[1], "/media/rawData/genomes/STAR_genomeDir_hg19_vGATK")
    # s.executeFunctions(command)
    deltaTime = time.time() - startTime
    print("Ran STAR on " + str(tupleOfFiles) + " for " + str(deltaTime) + " seconds")

def runStarSingleWrap(file):
    print("\n\n")
    startTime = time.time()
    star.runStar(file, genome = "/media/rawData/genomes/STAR_genomeDir_hg19_vGATK", cpu = numthreads)
    deltaTime = time.time() - startTime
    print('Ran STAR on %s for %s seconds.' % (file, deltaTime))

# Parallel(n_jobs=2)(delayed(runStarWrap)(i) for i in listOfFiles)

for x in fastqGzPairs:
    extractCommand = "zcat %s > %s"
    extractCommandList = []
    extractCommandList.append(extractCommand % (x[0], x[0]))
    extractCommandList.append(extractCommand % (x[1], x[1]))
    pool = ThreadPool(2)
    print("Extracting fastq file pair...")
    pool.map(s.executeFunctions,extractCommandList)
    # s.executeFunctions(extractCommand % (x[0], x[0]), captureOutput=False)
    # s.executeFunctions(extractCommand % (x[1], x[1]), captureOutput=False)
    print("Running STAR...")
    runStarPairWrap(x)
    s.executeFunctions("rm *.fastq")

# for x in singleFiles:
#     extractCommand = "zcat %s.gz > %s" % (x, x)
#     print("Extracting fastq files...")
#     s.executeFunctions(extractCommand)
#     print("Running STAR...")
#     runStarSingleWrap(x)
#     s.executeFunctions("rm *.fastq")
