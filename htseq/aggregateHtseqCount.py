import sys, os
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/htseq/")
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import htseq as h
import shellUtil as s
import glob

assert s.isStdInEmpty()

"""
Usage: 
python aggregateHtseqCount.py *.txt 
"""

args = sys.argv[1:]
assert len(args) == 1

files = glob.glob(args[0])
h.aggregateHtseqCountResults(files)
