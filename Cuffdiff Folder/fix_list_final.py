import os
import glob

def fileNames (diffPath):
    for path in diffPath:
        baseN = os.path.basename(path).split(".")[0]
        Order.append(baseN)
def MakeGenes (refseq, reflink): 
    with open(refseq, 'rU') as fileH:
        for line in fileH:
            access_list = []
            splitter = line.strip().split('\t')
            info = splitter[8].split(';')
            exonLength = int(splitter[4]) - int(splitter[3]) + 1
            for keys in info:
                accesskey = keys.split('"')
                if len(accesskey)>2:
                    access_list.append(accesskey[1])
            mergeDict.setdefault(access_list[0],[]).append([access_list[1],access_list[3],exonLength])
            if 'NM' not in access_list[3].split('_')[0]:
                accessOrf.setdefault(access_list[0],[]).append(exonLength)
    with open(reflink,'rU') as geneH:
        f = geneH.readline()
        for line in geneH:
            splitter = line.strip().split('\t')
            geneID = splitter[0].split(';')
            access = splitter[2]
            GeneNames[access] = geneID[0]
def WriteFiles(diffF):
    for i in range(len(Order)):
        CurrentFile = diffF[i]
        GroupName = Order[i]
        outputfile = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/' + GroupName + '_updated.txt' #path for new file produced
        output = open(outputfile,'w')
        with open(CurrentFile, 'rU') as filehandle:
            headline = filehandle.readline()
            output.write(headline)
            for line in filehandle:
                geneName = []
                finalGenes = []
                ExonLengths = []
                totalTran = []
                transcriptSeen = set()
                gene_seen = set()
                cut = line.strip().split('\t')
                xloc = cut[0]
                category = cut[14]
                trans_list = mergeDict.get(xloc,xloc)
                exonlist = accessOrf.get(xloc,"None")
                if "ProteinCoding" in category:
                    checkProt = None
                    for key in trans_list:
                        geneName.append(GeneNames.get(key[1],key[1]))
                        if 'NM' not in key[1].split('_')[0]:
                            if key[0] not in transcriptSeen:
                                totalTran.append(sum(ExonLengths))
                                ExonLengths = []
                                if key[2] > 200:
                                    totalTran.append(key[2])
                                else:
                                    ExonLengths.append(key[2])
                                transcriptSeen.add(key[0])
                            else:
                                ExonLengths.append(key[2])
                    for values in geneName:
                        if values not in gene_seen:
                            finalGenes.append(values)
                            gene_seen.add(values)
                    for lengths in totalTran:
                        if lengths > 200:
                             checkProt = 'ProteinCoding+lncRNA'
                    if 'None' not in exonlist:
                        for exons in exonlist:
                            if exons > 200:
                                checkProt = 'ProteinCoding+lncRNA'
                    if checkProt != None:
                        newline = '\t'.join(cut[0:14]) + '\t' + checkProt + '\t' + ', '.join(finalGenes) + '\t' +'\t'.join(cut[16:23]) +'\n'
                        output.write(newline)
                    else:
                        newline = '\t'.join(cut[0:15]) + '\t' + ', '.join(finalGenes) + '\t' + '\t'.join(cut[16:23]) + '\n'
                        output.write(newline)
                elif "Known_lncRNA" in category:
                    newCategory = None
                    checkLink = None
                    for key in trans_list:
                        geneName.append(GeneNames.get(key[1],key[1]))
                        checkProt = key[1].split('_')[0]
                        if 'NM' in checkProt:
                            newCategory = 'ProteinCoding'
                        elif 'NM' not in key[1].split('_')[0]:
                            if key[0] not in transcriptSeen:
                                totalTran.append(sum(ExonLengths))
                                ExonLengths = []
                                if key[2] > 200:
                                    totalTran.append(key[2])
                                else:
                                    ExonLengths.append(key[2])
                                transcriptSeen.add(key[0])
                            else:
                                ExonLengths.append(key[2])
                    for values in geneName:
                        if values not in gene_seen:
                            finalGenes.append(values)
                            gene_seen.add(values)
                    for lengths in totalTran: #takes all the exon total lengths and see if they add up >200 to be lncRNA
                        if lengths > 200:
                            checkLink = 'lncRNA'
                    if "None" not in exonlist: #check single exons could be greater than 200bp which automatically is lncRNA if true
                        for exons in exonlist:
                            if exons > 200:
                                checkLink = 'lncRNA'
                    if newCategory != None and checkLink != None: #check if knownlncrna = ProteinCoding+lncRNA
                        newline = '\t'.join(cut[0:14]) + '\t' + str(newCategory+ '+' + checkLink) + '\t' + ', '.join(finalGenes) + '\t' +'\t'.join(cut[16:23]) +'\n'
                        output.write(newline)
                    elif newCategory != None and checkLink == None: #check if knownlncRNA = PRoteinCoding
                        newline = '\t'.join(cut[0:14]) + '\t' + newCategory + '\t' + ', '.join(finalGenes) + '\t' +'\t'.join(cut[16:23]) +'\n'
                        output.write(newline)
                    elif newCategory == None and checkLink== None: #check if knownlncRNA < 200bp in transcripts
                        newline = '\t'.join(cut[0:14]) + '\t' + 'Other' + '\t' + ', '.join(finalGenes) + '\t' +'\t'.join(cut[16:23]) +'\n'
                        output.write(newline)
                    else:
                        output.write(line)
                else:
                    output.write(line)
        output.close()        

diffFiles = glob.glob('C:/Users/tony/Desktop/pythonAssign/Fix_Lists/*/*.diff') #location of file
mergeGenecod = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/Merge_gencodev19_refseq.combined.gtf'
linkF = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/refLink_08_12_15.txt' #location of the refLink file
Order = []
mergeDict = {}
GeneNames = {}
accessOrf = {}
fileNames(diffFiles)
MakeGenes(mergeGenecod, linkF)
WriteFiles(diffFiles)
