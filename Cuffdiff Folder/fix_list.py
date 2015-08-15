#!/usr/bin/env python3

import glob
import os

diffFiles = glob.glob('C:/Users/tony/Desktop/pythonAssign/Fix_Lists/*/*.diff') #location of file
mergeGenecod = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/Merge_gencodev19_refseq.combined.gtf' #location of mergeGeneCode file
linkF = 'C:/Users/tony/Desktop/pythonAssign/Fix_Lists/FOM_Project/refLink_08_12_15.txt' #location of the refLink file
Order = []
ValidationDic = {}
accessOrf = {}
GeneNames = {}

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
        accessOrf.setdefault(access_list[0],[]).append(orfLength)
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
            orf_list = accessOrf.get(xloc,"None")
            if "None" not in trans_list:
                if 'ProteinCoding' in category:
                    for key in trans_list:
                        geneName.append(GeneNames.get(key,key))
                    for values in geneName:
                        if values not in gene_seen:
                            finalset.append(values)
                            gene_seen.add(values)
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
                        newline = '\t'.join(cut[0:14]) + '\t' + newCategory + '\t' + ', '.join(finalset) + '\t' +'\t'.join(cut[16:23]) +'\n'
                        output.write(newline) 
                    else:
                        newCat = None
                        if "None" not in orf_list:
                            for length in orf_list:
                                if length > 200:
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

