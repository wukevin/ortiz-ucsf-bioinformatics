import sys, os, getopt
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
sys.path.append(os.environ['PIPELINEHOME'] + "/htseq/")
# sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/htseq/")
# sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import htseq as h
import shellUtil as s

# arguments = sys.argv[1:]

# if s.isStdInEmpty():
#   # Process command line args
#   if len(arguments) != 3:
#       print("Incorrect number of arguments")
#       print(helpDoc)
#   else:
#       if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1] and 'bam' in arguments[2]:
#           h.htseqWrapper(arguments[2], arguments[1])
#       else:
#           print("Wrong arguments")
#           print(helpDoc)
# else:
#   STDIN = s.getStdIn()
#   if arguments[0] == "--referenceGtf" and 'gtf' in arguments[1]:
#       h.htseqParallel(STDIN, arguments[1], threadCount = 16)
#   else:
#       print("Incorrect usage.")
#       print(helpDoc)

def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts=None, longopts = [
            'referenceGtf=', 'instances='])
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
