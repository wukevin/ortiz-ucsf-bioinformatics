
# test = subprocess.check_output('cgquery "participant_id=fc5b5d2f-0d03-45c2-b7a0-ba6ec108fe51&library_strategy=RNA-Seq"', shell = True)

import sys, subprocess, glob, os, getopt
sys.path.append(os.environ['PIPELINEHOME'] + "/util/")
import fileUtil as f
import shellUtil as s
import tcgaUtil as t

def main():
    try:
        optlist, args = getopt.getopt(args = sys.argv[1:], shortopts=None, longopts = [
            'download', 'keyfile='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    download = False
    keyfile = ""
    for o, a in optlist:
        if o == '--download':
            download = True
        elif o == '--keyfile':
            keyfile = a
    if download and len(keyfile) == 0:
        print("If downloading, you need a keyfile")
        return
    # print(args)
    if len(args) != 1:
        print("Must supply query string without spaces")
        return
    t.queryAndDownload(args[0], keyfile, download)
    

if __name__ == "__main__":
    main()
