#!/usr/bin/python3
import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import shellUtil as s
import tcgaUtil as t
import fileUtil as f
import os
import time
import glob
from multiprocessing import Pool as ThreadPool

helpDoc = """
"""

# def getBam(partialString):
#     for f in glob.glob('*.bam'):
#         if partialString in f:
#             return f

# idmapfile = open("/media/rawData/TCGA_SKCM/ids_to_filename.txt",'r')
# idDict = dict()
# for l in idmapfile:
    # parsed = l.split()
    # idDict[parsed[0]] = parsed[1]
# desiredIDsFile = open("NRAS_Q61_barcodes.txt", 'r')
# desiredIDs = []
# for l in desiredIDsFile:
    # desiredIDs.append(idDict[l.strip()])
# print(desiredIDs)
def runCufflinks(bamfileprefix, refGtf):
    bamfile = f.getBam(bamfileprefix)# bamfileprefix + "_Aligned.sortedByCoord.out.bam"
    if os.path.isfile(bamfile+".bai") == False:
        print("The bam does not have a index file. Generating one now...")
        s.executeFunctions("samtools index " + bamfile)
    s.executeFunctions("mkdir %s" % (bamfile + '_cufflinks'))
    command = 'cufflinks --verbose -p 4 -o %s -G %s %s' % (bamfile + '_cufflinks', refGtf, bamfile)
    print(command)
    startTime = time.time()
    result = s.executeFunctions(command, captureOutput = True)
    resultFile = open(bamfile + '_cufflinks/log.txt', mode = 'w')
    resultFile.write(result)
    resultFile.close()
    print("Finished cufflinks run in %s seconds" % (time.time()-startTime))
    return result

def runCufflinksWrapper(tupleOfArgs):
    print(tupleOfArgs)
    return runCufflinks(tupleOfArgs[0], tupleOfArgs[1])

# results = pool.map(runCufflinks, desiredIDs)

#for id in desiredIDs:
#    bamfile = getBam(id)
#    foldername = "cufflinks_run2/%s_cufflinks" % bamfile
#    if os.path.exists(foldername):
#        continue
#    print(foldername)
def main():
    # if s.isStdInEmpty():
    #     # Process command line args
    #     print("No StdIn")
    #     print(helpDoc)
    # elif len(sys.argv) != 3:
    #     print("Incorrect number of arguments")
    #     print(helpDoc)
    # else:
    #     referenceGtf = ''
    #     if len(sys.argv) == 3 and sys.argv[1] == '--referenceGtf':
    #         referenceGtf = sys.argv[2]
    #     stdin = s.getStdIn()
    #     filePrefixes = t.getPrefixForIDs(stdin)
    #     # Generate input tuples for pool.map
    #     inTup = []
    #     for f in filePrefixes:
    #         inTup.append((f,referenceGtf))
    #     pool.map(runCufflinksWrapper, inTup)
    # python runCufflinks.py --referenceGtf xxx.gtf *.bam
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts=None, longopts = [
            'referenceGtf='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    refGtf = ""
    for o, a in optlist:
        if o == '--referenceGtf':
            refGtf = a
    if len(args) == 0:
        print("No bam/sam files provided. Exiting...")
        sys.exit(2)
    pool = ThreadPool(4)
    inTup = []
    for f in args:
        inTup.append((f,refGtf))
    pool.map(runCufflinksWrapper, inTup)



if __name__ == '__main__':
    main()


# print(len(sys.argv))
