#!/usr/bin/env python3

import glob
import os

diffFiles = glob.glob('C:/Users/tony/Desktop/pythonAssign/Fix_Lists/*/*.diff') #location of file
mergeGenecod = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/Merge_gencodev19_refseq.combined.gtf' #location of mergeGeneCode file
linkF = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/refLink_08_12_15.txt' #location of the refLink file
Order = []
ValidationDic = {}
accessExons = {}
GeneNames = {}
accessTranscripts = {}

for path in diffFiles: #creates order of the files read and produced
    fileName = os.path.basename(path)
    base = fileName.split(".")[0]
    Order.append(base)


with open(mergeGenecod, 'rU') as fileH: 
    for line in fileH:
        access_list = []
        splitter = line.strip().split('\t')
        info = splitter[8].split(';')
        orfLength = int(splitter[4]) - int(splitter[3]) + 1
        for keys in info:
            accesskey = keys.split('"')
            if len(accesskey) > 2:
                access_list.append(accesskey[1])
        ValidationDic.setdefault(access_list[0],[]).append(access_list[3])
        accessExons.setdefault(access_list[0],[]).append(int(orfLength))
        accessTranscripts.setdefault(access_list[3],[]).append(int(orfLength))
with open(linkF, 'rU') as geneH:
    f = geneH.readline()
    for line in geneH:
        splitter = line.strip().split('\t')
        geneID = splitter[0].split(';')
        access = splitter[2]
        GeneNames[access] = geneID[0]
for i in range(len(Order)):
    CurrentFile = diffFiles[i]
    GroupName = Order[i]
    outputfile = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/' + GroupName + '_updated.txt' #path for new file produced
    output = open(outputfile,'w')
    with open(CurrentFile,'rU') as standard: #opens current file
        headline = standard.readline()
        output.write(headline)
        for line in standard:
            geneName = []
            finalset = []
            gene_seen = set()
            cut = line.strip().split('\t')
            xloc = cut[0]
            category = cut[14]
            trans_list = ValidationDic.get(xloc,"None")
            exon_list = accessExons.get(xloc,"None")
            if "None" not in trans_list:
                if 'ProteinCoding' in category:
                    check4link = None
                    for key in trans_list:
                        checkProt = key.split('_')[0]
                        if 'NR' in checkProt:
                            linkLength = accessTranscripts.get(key[0],0)
                            if linkLength > 200:
                                geneName.append(str(GeneNames.get(key,key) + '(lncRNA)'))
                                check4link = 'Protein+lncRNA'
                            else:
                                geneName.append(GeneNames.get(key,key))
                        else:
                            geneName.append(GeneNames.get(key,key))
                    for values in geneName:
                        if values not in gene_seen:
                            finalset.append(values)
                            gene_seen.add(values)
                    if check4link != None:
                        newline = '\t'.join(cut[0:14]) + '\t' + check4link +'\t' + ', '.join(finalset) + '\t' + '\t'.join(cut[16:23]) + '\n'
                        output.write(newline)
                    else:
                        newline = '\t'.join(cut[0:15]) + '\t' + ', '.join(finalset) + '\t' + '\t'.join(cut[16:23]) + '\n'
                        output.write(newline)
                elif 'Known_lncRNA' in category:
                    newCategory = None
                    for key in trans_list:
                        geneName.append(GeneNames.get(key,key))
                        checkProt = key.split('_')[0]
                        if 'NM' in checkProt:
                            newCategory = 'ProteinCoding'
                    for values in geneName:
                        if values not in gene_seen:
                            finalset.append(values)
                            gene_seen.add(values)
                    if newCategory != None:
                        newGenes = []
                        newFinalset = []
                        new_seen = set()
                        check4link = None
                        for key in trans_list:
                            checkProt = key.split('_')[0]
                            if 'NR' in checkProt:
                                linkLength = accessTranscripts.get(key[0],0)
                                if linkLength > 200:
                                    newGenes.append(str(GeneNames.get(key,key) + '(lncRNA)'))
                                    check4link = 'Protein+lncRNA'
                                else:
                                    newGenes.append(GeneNames.get(key,key))
                            else:
                                newGenes.append(GeneNames.get(key,key))
                        for values in newGenes:
                            if values not in new_seen:
                                newFinalset.append(values)
                                new_seen.add(values)
                        if check4link != None:
                            newline = '\t'.join(cut[0:14]) + '\t' + check4link + '\t' + ', '.join(newFinalset) + '\t' +'\t'.join(cut[16:23]) +'\n'
                            output.write(newline)
                        else:
                            newline = '\t'.join(cut[0:14]) + '\t' + newCategory + '\t' + ', '.join(finalset) + '\t' +'\t'.join(cut[16:23]) +'\n'
                            output.write(newline) 
                    else:
                        newCat = None
                        if "None" not in exon_list:
                            if sum(exon_list) > 200:
                                newCat = 'check'
                            if newCat == None:
                                realCat = "Other"
                                newline = '\t'.join(cut[0:14]) + '\t' + realCat + '\t' + ', '.join(finalset) + '\t' +'\t'.join(cut[16:23]) +'\n'
                                output.write(newline)
                            else:
                                newline = '\t'.join(cut[0:15]) + '\t' + ', '.join(finalset) + '\t' + '\t'.join(cut[16:23]) + '\n'
                                output.write(newline)
                        else:
                            newline = '\t'.join(cut[0:15]) + '\t' + ', '.join(finalset) + '\t' + '\t'.join(cut[16:23]) + '\n'
                            output.write(newline)
                else:
                    output.write(line)
            else:
                output.write(line)
    output.close()

