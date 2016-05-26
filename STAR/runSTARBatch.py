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
import getopt

from multiprocessing import Pool as ThreadPool

# k.runKallistoManualLength()
# numthreads = max(s.getAvailableThreads(), 12)
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
# fastqGzFiles = glob.glob("*.fastq.gz")
# fastqGzPairs = f.pairGivenFastqFiles(fastqGzFiles)

# pairFiles = []
# singleFiles = []
# for x in listOfPrefixes:
#     if os.path.isfile(x + "_2.fastq"):
#         pairFiles.append((x + "_1.fastq", x + "_2.fastq"))
#     else:
#         singleFiles.append(x + "_1.fastq")
# listOfFiles = [(x + "_1.fastq", x + "_2.fastq") for x in listOfPrefixes]

import time

def runStarPairWrap(tupleOfFiles, genome, numthreads = 16):
    print("\n\n")
    startTime = time.time()
    print("Starting STAR run on %s and %s" % tupleOfFiles)
    result = star.runStar(tupleOfFiles[0], tupleOfFiles[1], genome, cpu = numthreads)
    if result != None:
        logfile = open(f.longestCommonSubstring(tupleOfFiles[0], tupleOfFiles[1]) + '.star.log', 'w')
        logfile.write(result)
        logfile.close()
    # command = "python runSTAR.py %s %s %s" % (tupleOfFiles[0], tupleOfFiles[1], "/media/rawData/genomes/STAR_genomeDir_hg19_vGATK")
    deltaTime = time.time() - startTime
    print("Ran STAR on " + str(tupleOfFiles) + " for " + str(deltaTime) + " seconds")

def runStarSingleWrap(file, numthreads = 12):
    print("\n\n")
    startTime = time.time()
    star.runStar(file, genome = "/media/rawData/genomes/STAR_genomeDir_hg19_vGATK", cpu = numthreads)
    deltaTime = time.time() - startTime
    print('Ran STAR on %s for %s seconds.' % (file, deltaTime))

# Parallel(n_jobs=2)(delayed(runStarWrap)(i) for i in listOfFiles)

def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts=None, longopts = [
            'genomeDir='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    genomeDir = ""
    for o, a in optlist:
        if o == '--genomeDir':
            genomeDir = a
    if len(args) == 0:
        print("No fastq files given. Exiting.")
        sys.exit(2)
    if len(genomeDir) == 0:
        print("No genome directory specified. Exiting.")
        sys.exit(2)

    pairedFiles = f.pairGivenFastqFiles(args)
    for x in pairedFiles:
        extractedFiles = (x[0][:len(x[0]) - 3], x[1][:len(x[1]) - 3])
        if os.path.isfile(extractedFiles[0]) != True or os.path.isfile(extractedFiles[1]) != True:
            extractCommand = "zcat %s > %s"
            extractCommandList = []
            extractCommandList.append(extractCommand % (x[0], extractedFiles[0]))
            extractCommandList.append(extractCommand % (x[1], extractedFiles[1]))
            pool = ThreadPool(2)
            print("Extracting fastq file pair...")
            pool.map(s.executeFunctions,extractCommandList)
        else:
            print("Fastq files already extracted.")
        # s.executeFunctions(extractCommand % (x[0], x[0]), captureOutput=False)
        # s.executeFunctions(extractCommand % (x[1], x[1]), captureOutput=False)
        # print("Running STAR on %s and %s" % (extractedFiles))
        runStarPairWrap(extractedFiles, genomeDir)
        s.executeFunctions("rm *.fastq")
    star.unloadGenome(genomeDir)

if __name__ == '__main__':
    main()
# for x in singleFiles:
#     extractCommand = "zcat %s.gz > %s" % (x, x)
#     print("Extracting fastq files...")
#     s.executeFunctions(extractCommand)
#     print("Running STAR...")
#     runStarSingleWrap(x)
#     s.executeFunctions("rm *.fastq")
