import os
import sys
import getopt
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

helpDoc = """

"""


def executeTrinityGenomeGuided(bamfile):
    outputFolder = bamfile[:-4] + '_trinity_Out'
    logfile = outputFolder + '/trinity.log'
    template = "trinity --genome_guided_bam %s --genome_guided_max_intron 11000 --max_memory 54G --CPU 16 --output %s" % (
        bamfile, outputFolder)
    s.executeFunctions(template)


def executeTrinityFastq(fastq1, fastq2, n, rerun = False):
    extracting = False
    # If in gz format, extract such that trintiy can run on it
    if 'gz' in fastq1 and 'gz' in fastq2:
        extracting = True
    if extracting is True:
        print("Extracting files")
        s.extractGz([fastq1, fastq2])
        fastq1 = fastq1[:-3]
        fastq2 = fastq2[:-3]
        print("Finished extraction. Set new file pointers to %s and %s" %
              (fastq1, fastq2))
    # Sanity test
    assert '_1' in fastq1
    assert '_2' in fastq2
    # Run trinity
    lcs = f.longestCommonSubstring(fastq1, fastq2)
    # outputFolder = lcs + '_trinity_Out'
    outputFolder = lcs + '_trinity_out'
    # Check if result already exists; if so, don't rerun
    if rerun == False and os.path.isfile(outputFolder + '.Trinity.fasta'):
        print(outputFolder + '.Trinity.fasta already exists. Not rerunning.' )
        return None
    # logfile = outputFolder + '/trinity.log'
    logfile = lcs + ".Trinity.log"
    template = 'trinity --seqType fq --full_cleanup --verbose --left %s --right %s --max_memory 54G --CPU %s --output %s' % (
        fastq1, fastq2, n, outputFolder)
    result = s.executeFunctions(template, captureOutput=True)
    # Write console log to logfile
    log = open(logfile, mode='w')
    log.write(result)
    log.close()
    # if we extracted earlier, remove the extracted fastq files to save sapce
    if extracting:
        s.executeFunctions('rm ' + fastq1)
        s.executeFunctions('rm ' + fastq2)


def main():
    # Get options
    try:
        optlist, args = getopt.getopt(args=sys.argv[1:], shortopts=None, longopts=[
                                      'all-files', 'genome-guided', 'cpu='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    runAll = False
    fq = True
    threadCount = 16  # Default to 16 threads
    files = []
    # Walk thorugh given options
    for o, a in optlist:
        if o == '--all-files':
            runAll = True
        elif o == '--genome-guided':
            fq = False
        if o == '--cpu':
            threadCount = a

    # Caution: this section is not 100% done. Only enough to run what I need right now.
    # Run the wrappers
    if runAll is True:
        assert len(args) == 0
        pairs = f.getFastqPairs()
        # Walk through every pair in this dir
        for pair in pairs:
            print(pair)
            assert len(pair) == 2
            x, y = None, None
            if "_1" in pair[0]:
                x, y = pair[0], pair[1]
            else:
                x, y = pair[1], pair[0]
            print("Running trinity on\n%s\n%s" % (x, y))
            executeTrinityFastq(x, y, threadCount)

if __name__ == "__main__":
    main()
