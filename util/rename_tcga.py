import sys, os
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
import shellUtil as s
import tcgaUtil as t
import glob
import getopt

files = glob.glob("*.bam")
# print(files)

def fileRename(suffix, sim):
    files = glob.glob("*" + suffix)
    logfile = open("rename.mapping", mode = "w")
    for f in files:
        TCGA_ID = t.getMetadataFromSequenceFilename(f)
        destination = TCGA_ID + suffix
        logfile.write(f + '\t' + destination + '\n')
        if sim:
            continue
        os.rename(f, destination)
    logfile.close()

# suffix = ".Aligned.soortedByCoord.bam"
# logfile = open("rename.mapping", mode = "w") # Open to write
# for f in files:
#     TCGA_ID = t.getMetadataFromSequenceFilename(f)
#     destination = TCGA_ID + suffix
#     logfile.write(f + '\t' + destination + '\n')
#     os.rename(f, destination)
# logfile.close()


def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts = None, longopts = ['suffix=', 'simulate'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    suffix = '.bam'
    simulate = False
    for o, a in optlist:
        # print(o)
        if o == '--suffix':
            suffix = a
        elif o == '--simulate':
            simulate = True
        else:
            print("Unrecognized option: " + o)
            sys.exit(2)
    fileRename(suffix, simulate)


if __name__ == '__main__':
    main()
