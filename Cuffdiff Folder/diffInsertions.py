#!/usr/bin/env python3
# Name: Tony Li
import glob
import sys
import os

class AddColumns:
    Order = [] #should always be in this order if anything just look at data and change name if needed
    bedChromInfo = {}
    def median(listy):
        listy = [float(x) for x in listy]
        listy=sorted(listy)
        if len(listy)%2 == 1:
            #Odd
            Number = len(listy)//2
            Number = listy[Number]
        else:
            #Even
            Second=len(listy)//2
            First = len(listy)//2
            First = First-1
            Number = (listy[First]+listy[Second])/2
        return Number
    def addFPKM(tracker,info,export,link,bed):
        #take (BRAf, mel, nras) groups 3 files at a time and output a file at atime
        linkInfo = {}
        for fileloc in export:
            os.path.dirname(fileloc)
            fileName = os.path.basename(fileloc)
            baseName = fileName.split(".")
            AddColumns.Order.append(baseName[0])
        with open(link,'rU') as genehandle: #uses the reflink file to match each geneName with the accession number
            f = genehandle.readline()
            for line in genehandle:
                cut = line.strip().split('\t')
                geneID = cut[0]
                access = cut[2].split('_')
                if 'NM' in access[0]:
                    linkInfo['_'.join(access)] = geneID
        with open(bed,'rU') as fileH: #uses the refGene bed file to create dictionaries
            for line in fileH:
                splitted = line.strip().split('\t')
                chrom = splitted[0].split('_')
                accesskey = splitted[3].split('_')
                geneStart = int(splitted[1])
                geneStop = int(splitted[2])
                if len(chrom) <= 1:
                    if 'NM' in accesskey[0]:
                        geneName = linkInfo.get('_'.join(accesskey),'_'.join(accesskey))
                        AddColumns.bedChromInfo.setdefault(chrom[0],{}).setdefault(geneName,(geneStart,geneStop))
        for i in range(len(AddColumns.Order)):
            #lists and dictionaries that needs to be emptied out after every group run, there are three groups (BRAF, Mel, NRAS)
            melanomaStrains = []
            MelDic = {}
            FOMDic = {}
            Current_Tracker = tracker[i]
            Current_Info = info[i]
            Current_Export = export[i]
            Group = AddColumns.Order[i]
            outputfile = Group + '_updated.txt'
            output = open(outputfile, 'w')
            with open(Current_Info,'rU') as filehandle: #takes Current_Info file from either braf, nras, mel and creates a list of melanoma strains
                fifi = filehandle.readline()
                for line in filehandle:
                    usuable_lines = line[1:]
                    cuttabs = usuable_lines.strip().split('\t')
                    cutSlashes = cuttabs[0].split('/')
                    if 'FOM' in cutSlashes[3]:
                        pass
                    else:
                        melanomaStrains.append(cutSlashes[3])                   
            with open(Current_Tracker, 'rU') as fileH: #takes Current_Tracker file from either braf, nras, mel and creates a FOM dictionary and melanoma dictionary with the FPKMs of each strain
                f = fileH.readline()
                for line in fileH:
                    cutter = line.strip().split('\t')
                    geneID = cutter[0]
                    Type = cutter[1]
                    splitCellname = Type.split('_')
                    cellType = splitCellname[0]
                    replicate = int(cutter[2])
                    FPKM = str(cutter[6])
                    if 'FOM' in cellType:
                        FOMDic[geneID] = FPKM
                    elif 'Melanoma' in cellType:
                        MelDic.setdefault(geneID,{}).setdefault(replicate,[]).append(FPKM)
                    else:
                        pass
            with open(Current_Export,'rU') as infile: #uses fom/mel dictionarys and the melanoma strains list to generate columns with the fpkm corresponding to each strain + the median of the fpkm excluding fom
                f = infile.readline()
                headline = f.strip().split('\t')
                globalHead = '\t'.join(headline) + '\t' + 'FOM' + '\t'+'\t'.join(melanomaStrains) + '\t' + 'Melanoma Median' + '\t' + 'Non-Zero FPKMs' + '\t' + 'Category' + '\t' + 'Associated Genes' + '\t' + 'Gene Distances\n'
                output.write(globalHead)
                start = globalHead.strip().split('\t').index("FOM") + 1
                end = globalHead.strip().split('\t').index("Melanoma Median")
                for line in infile:
                    FPKMlist = []
                    non_zero = 0
                    splitter = line.strip().split('\t')
                    geneID = splitter[0]
                    FOMfpkm = FOMDic[geneID]
                    FPKMlist.append(FOMfpkm)
                    for strain in range(len(melanomaStrains)):
                        Melfpkm = MelDic[geneID][strain][0]
                        FPKMlist.append(Melfpkm)
                    med = str(AddColumns.median(FPKMlist))
                    FPKMline = '\t'.join(splitter) + '\t' + '\t'.join(FPKMlist) + '\t' + med +'\n'
                    readFPKM = FPKMline.strip().split('\t')
                    for FPKM in readFPKM[start:end]:
                        number = float(FPKM)
                        if number > 0:
                            non_zero += 1
                    newline = '\t'.join(readFPKM) + '\t' + str(non_zero)
                    finalLine = AddColumns.addCategories(newline)
                    output.write(finalLine)
        output.close()
    def addCategories(line):
        geneOverlap = []
        sortter = []
        maxlist = []
        minlist = []
        cuttabs = line.strip().split('\t')
        lncrna = cuttabs[0].split('_')
        locus = cuttabs[3].split(':')
        chrom = locus[0].split('_')
        geneLength = locus[1].split('-')
        lncrnaStart = int(geneLength[0])
        lncrnaStop = int(geneLength[1])
        if len(lncrna) > 2: #for only lncrnas
            if len(chrom) <= 1: #for only chromosomes(not sub-chromosomes)
                for gene, orf in AddColumns.bedChromInfo[chrom[0]].items():
                    if (min(orf[1],lncrnaStop) - max(orf[0],lncrnaStart)) > 0:
                        geneOverlap.append([gene,orf[0],orf[1]])
                if len(geneOverlap) > 1: #multiple overlaps
                    geneOverlap.sort(key = lambda x: x[1])
                    for g in range(len(geneOverlap)):
                        sortter.append(geneOverlap[g][0])
                    overlaps = ','.join(sortter[1:-2])
                    leftgene = sortter[0] + ' (Leftmost)'
                    rightgene = sortter[-1] + ' (Rightmost)'
                    newline = '\t'.join(cuttabs) + '\t' + 'Multiple Overlap ' + '\t' +','.join([leftgene,rightgene,overlaps]) + '\t' + 'N/A' + '\n'
                    return newline
                elif len(geneOverlap) == 1:
                    if lncrnaStart < geneOverlap[0][1] and lncrnaStop <= geneOverlap[0][2]: #intronic to the right
                        for gene,orf in AddColumns.bedChromInfo[chrom[0]].items():
                            if geneOverlap[0][1] > orf[1]:
                                sortter.append([gene,orf[1]])
                        sortter.sort(key= lambda x:x[1])
                        leftgene = str(sortter[-1][0]) + ' (Leftmost)'
                        rightgene = str(geneOverlap[0][0]) + ' (Rightmost)'
                        distance = str(lncrnaStart - int(sortter[-1][1]) + 1)
                        newline = '\t'.join(cuttabs) + '\t' + 'Intronic to Right' + '\t' + ','.join([leftgene,rightgene]) + '\t' + distance + '\n'
                        return newline
                    elif lncrnaStart >= geneOverlap[0][1] and lncrnaStop > geneOverlap[0][2]: #intronic to the left
                        for gene,orf in AddColumns.bedChromInfo[chrom[0]].items():
                            if geneOverlap[0][2] < orf[0]:
                                sortter.append([gene,orf[0]])
                        sortter.sort(key= lambda x:x[1])
                        rightgene = str(sortter[0][0]) + ' (Rightmost)'
                        leftgene = str(geneOverlap[0][0]) + ' (Leftmost)'
                        distance = str(int(sortter[0][1]) - lncrnaStop + 1)
                        newline = '\t'.join(cuttabs) + '\t' + 'Intronic to Left' + '\t' + ','.join([leftgene,rightgene]) + '\t' + distance + '\n'
                        return newline
                    elif lncrnaStart >= geneOverlap[0][1] and lncrnaStop <= geneOverlap[0][2]: #intronic overlapped
                        newline = '\t'.join(cuttabs) + '\t' + '\t'.join(['Intronic',geneOverlap[0][0],'N/A']) + '\n'
                        return newline
                    else: #intronic leftovers
                        newline = '\t'.join(cuttabs) + '\t' + '\t'.join(['lncRNA Greater than Gene',geneOverlap[0][0],'N/A']) + '\n'
                        return newline
                else: #intergenic or unknown lncrna
                    for gene, orf in AddColumns.bedChromInfo[chrom[0]].items():
                        if lncrnaStart >= orf[1]:
                            maxlist.append([gene,orf[1]])
                        elif lncrnaStop <= orf[0]:
                            minlist.append([gene,orf[0]])
                    if len(maxlist) >= 1 and len(minlist) >= 1:
                        maxlist.sort(key= lambda x:x[1])
                        minlist.sort(key= lambda x:x[1])
                        leftgene = str(maxlist[-1][0]) + ' (Leftmost)'
                        rightgene = str(minlist[0][0]) + ' (Rightmost)'
                        leftdistance = str(lncrnaStart - int(maxlist[-1][1]) + 1) + ' (left)'
                        rightdistance = str(int(minlist[0][1]) - lncrnaStop + 1) + ' (right)'
                        newline = '\t'.join(cuttabs) +'\t' +  '\t'.join(['Intergenic',','.join([leftgene,rightgene]),','.join([leftdistance,rightdistance])]) + '\n'
                        return newline
                    else:
                        newline = '\t'.join(cuttabs) + '\t' + '\t'.join(['N/A','N/A','N/A']) + '\n'
                        return newline
            else: # for all other sub chromosomes with lncrna
                newline = '\t'.join(cuttabs) + '\t' + '\t'.join(['N/A','N/A','N/A']) + '\n'
                return newline
        else: #the rest of the stuff
            newline = '\t'.join(cuttabs) + '\t' + '\t'.join(['N/A','N/A','N/A']) + '\n'
            return newline
def startHelp():
    print("Parameters are as followed: python .py .diff file tracking file .info file .bed file refLink file \n")
    print("Need all five files and in order to generate any addtional files\n")
    print("First parameter: .diff file <indicate path of file> ")
    print("only one parameter and can take in multiple files using glob syntax.\n")
    print("Second parameter: .read_group_tracking file <indicate path of file> ")
    print("only one parameter and can take in multiple files using glob syntax.\n")
    print("Third parameter: group.info file <indicate path of file> ")
    print("only one parameter and can take in multiple files using glob syntax.\n")
    print("Fourth parameter: .bed file <indicate path of file> ")
    print("only one parameter and can take only one file.\n")
    print("Fifth parameter: refLink file <indicate path of file> ")
    print("only one parameter and can take only one file.\n")
def main(userIn):
    if len(userIn) == 6:
        inputFiles = glob.glob(str(userIn[1])) #diff files you want to convert
        trackInput = glob.glob(str(userIn[2])) #expression files
        infoInput = glob.glob(str(userIn[3])) #strain file
        bedFile = str(userIn[4]) #human genome gene reference file
        linkFile = str(userIn[5]) #human genome gene name conversion
        AddColumns.addFPKM(trackInput,infoInput,inputFiles,linkFile,bedFile)
    elif "getHelp" in userIn[1]:
        startHelp()
    else:
        raise Exception ("Parameters not placed correctly.")
try:
    main(sys.argv)
except:
    print ("Unexpected error:", sys.exc_info()[0])
    print ("Type getHelp for more info")
