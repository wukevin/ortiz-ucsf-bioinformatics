import sys, os
sys.path.append(os.environ['PIPELINEHOME'] + "/cufflinks/")
import cuffsuite as cuff

cuff.aggregateCufflinksResults()
