############ Original bash code ############
# Clean the transcripts
# seqclean Trinity-GG.fasta -c 16
# Of 25 commands, we want to run 1-14, and 16-25, skipping 15
# Command 15 is "descriptions of alignment assemblies and how they were constructed from the underlying transcript alignments" and always hangs the computer
# Creates db, runs 1-14 and does not execute 15
# $PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -C -r -R -g /home/ortiz-lab/Downloads/hg19/hg19.fa -t Trinity-GG.fasta.clean -T -u Trinity-GG.fasta --ALIGNERS gmap --CPU 16 -e 15 | tee log_cmd1-14
# Restarts at command 16
# $PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -R -g /home/ortiz-lab/Downloads/hg19/hg19.fa -t Trinity-GG.fasta.clean -T -u Trinity-GG.fasta --ALIGNERS gmap --CPU 16 -s 16 | tee log_cmd16-25
# Formerly used the hg19.fa in the downloads folder, now using the hg19 in /media/Data/genomes/

import sys, os
import fileUtil as f
import shellUtil as s
from multiprocessing import Pool as ThreadPool

def runSeqclean(fastaFile, numThreads = 16):
    command = "seqclean %s -c %s -r -o" % (fastaFile, numThreads)
    s.executeFunctions(command, captureOutput = True)
    cleanedFasta = fastaFile + ".clean"
    return cleanedFasta

def symlinkPasaConfig():
    if os.path.exists("alignAssembly.config"):
        print("Config file already exists. Not symlinking...")
        return None
    symlink = "ln -s /home/ortiz-lab/Documents/kwu/scripts/pasa/alignAssembly.config ./"
    s.executeFunctions(symlink)

def pasa(file, clean, referenceGenome, cpu):
    if clean:
        print("Cleaning " + file)
        cleanedFasta = runSeqclean(file, cpu)
    symlinkPasaConfig()
    command1Template = "$PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -C -r -R -g %s --ALIGNERS gmap --CPU %s -e 15" % (referenceGenome, cpu)
    command2Template = "$PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -R -g %s --ALIGNERS gmap --CPU %s -s 16" % (referenceGenome, cpu)
    if clean:
        suffix = " -T %s -u %s" % (cleanedFasta, file) # The space in front is very important
    else:
        suffix = " -t %s" % file
    command1 = command1Template + suffix
    s.executeFunctions(command1)
    command2 = command2Template + suffix
    s.executeFunctions(command2)
    return None

def main():
    try:
        optlist, args = getopt.getopt(args=sys.argv[1:], shortopts=None, longopts=[
                                      'seqclean', 'cpu=', 'referenceGenome='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    clean = False
    cpu = 16
    referenceGenome = "/media/rawData/genomes/hg19_gmap/hg19.fa"
    for o, a in optlist:
        if o == "--seqclean":
            clean = True
        elif o == "--cpu":
            cpu = int(a)
        elif o == "--referenceGenome":
            referenceGenome = a

    inputFiles = args
    for fastaFile in inputFiles:
        pasa(fastaFile, clean, referenceGenome, cpu)


if __name__ == '__main__':
    main()
