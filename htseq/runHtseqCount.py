import sys, os, getopt
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
sys.path.append(os.environ['PIPELINEHOME'] + "/htseq/")
# sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/htseq/")
# sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import htseq as h
import shellUtil as s

def help():
    helpString = """ Wrapper for htseq-count. Takes in two arguments:
                     --referenceGtf assembly.gtf (mandatory)
                     --instances <INT> (optional, defaults to 16)"""

def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts=None, longopts = [
            'referenceGtf=', 'instances=', 'help'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    instances = 16
    referenceGtf = ""
    for o, a in optlist:
        if o == "--referenceGtf":
            referenceGtf = a
        elif o == "--instances":
            instances = int(a)
        elif o == "--help" or o == '-h':
            help()
            sys.exit()
    # Check that all args are bam files
    for arg in args:
        if ".bam" not in arg:
            print("Arguments must all be bam files")
            sys.exit(2)
    if len(referenceGtf) == 0:
        print("Must supply reference gtf")
        sys.exit(2)
    logfile = open("command_history.log", "w")
    logfile.write("htseq-count using reference: %s" % referenceGtf)
    logfile.close()
    h.htseqParallel(args, referenceGtf, instances)


if __name__ == '__main__':
    main()
