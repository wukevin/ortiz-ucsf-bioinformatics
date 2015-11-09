
# test = subprocess.check_output('cgquery "participant_id=fc5b5d2f-0d03-45c2-b7a0-ba6ec108fe51&library_strategy=RNA-Seq"', shell = True)

import sys, subprocess
sys.path.append("/home/ortiz-lab/Documents/kwu/scripts/util/")
import fileUtil as f
import shellUtil as s

def getAnalysisIDs(participant_id): 
    commandTemplate = 'cgquery "participant_id=%s&library_strategy=RNA-Seq"'
    command = commandTemplate % (participant_id)
    print(command)
    output = subprocess.check_output(command, shell = True).splitlines()
    ids = []
    for line in output:
        if "analysis_id" in line:
            tokens = line.split(":")
            tokens = [x.strip() for x in tokens]
            ids.append(tokens[1])
    return ids

def downloadFromAnalysisID(analysis_id, keyFile="/media/Data2/TCGA_SKCM/cghub.key"):
    commandTemplate = ' gtdownload -v -c %s -d %s'
    command = commandTemplate % (keyFile, analysis_id)
    print(command)
    # s.executeFunctions(command, simulate = True, captureOutput = False)

# if (s.isStdInEmpty()):
#     if len(sys.argv) < 2:
#         print("You need to input something.")
# else:
#     stdin = s.getStdIn()
#     for x in stdin:
#         ids = getAnalysisIDs(x)
#         for y in ids:
#             downloadFromAnalysisID(y)

def queryAndDownload(queryString, keyfile):
    queryCommand = 'cgquery -o temp.xml "%s"' % (queryString)
    s.executeFunctions(queryCommand)
    downloadCommand = 'gtdownload -vv -c %s -d temp.xml' %s (keyfile)
