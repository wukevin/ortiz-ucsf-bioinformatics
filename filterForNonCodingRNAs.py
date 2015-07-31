

# 5/20/15
# Filter FOM-E, FOM-Q61, D04N, mm415N cufflinks assembled transcripts
# Keep all original filters




# See most recent^
# 4/14/15
# Filter FOM, FOM-E, FOM-Q61 assembled transcripts
# uploaded transcripts.gtf files to UCSC, downloaded as .bed files
# Removed Min. Intron Size requirement
# Changed min. total length from 160 to 200

##############


# TODO : 
# does it work?
#    -- what is output
#    -- how does it look on UCSC
# filter by size and require multiple exons
# convert to pattern recognition to do all files at once.
# send out results and post to genome browser for all

# EXPERIMENTS = ["FOM_E", "FOM_Q61", "D04N", "mm415N"]
EXPERIMENTS = ["FOM_Q61"]
BED_FILE_TO_FILTER = "%s_cufflinks_transcripts.bed"
OUTPUT_NAME_EXON_EXACT = "%s_cufflinks_transcripts_exonExact.bed"
OUTPUT_NAME_EXON_PARTIAL = "%s_cufflinks_transcripts_exonPartial.bed"
OUTPUT_NAME_EXON_NONE_KNOWN = "%s_cufflinks_transcripts_exonNone_known.bed"
OUTPUT_NAME_EXON_NONE_NOVEL = "%s_cufflinks_transcripts_exonNone_novel.bed"



REFSEQ_BED_FILE = "/Users/susanaortiz-urda/Klai/Common_lncRNA_Project_Cufflinks_Assembled_Only/RefGene_01162015.bed"
#Do not change below here unless something is wrong when running the script
MINIMUM_TOTAL_LENGTH = 200
MINIMUM_INTRON_SIZE = 10
OVERLAP_EXACT = 0
OVERLAP_PARTIAL = 1
OVERLAP_NONE = 2

TRACK_LINE_PATTERN = "track name='%s' description='%s' useScore=1\n"

def getExonStartStopsFromBedLine(line):
    pieces = line.split()
    start = int(pieces[1])
    blockSizes = pieces[10].split(",")[:-1]
    blockStarts = pieces[11].split(",")[:-1]
    
    retVal = []
    for i in range(len(blockSizes)):
        blockStart = start + int(blockStarts[i])
        blockStop = blockStart + int(blockSizes[i])
        retVal.append( (blockStart, blockStop) )

    return retVal

def getIntronSizes(startStops):
    
    intronSizes = []
    previousStop = startStops[0][1]
    for (start, stop) in startStops[1:]:
        intronSizes.append( start - previousStop )
        previousStop = stop

    return intronSizes

# read in all the RefSeq entries for gene (NM_) and RNA (NR_) entries into a list
# of exon start/stops per chromosome
def getRefSeqExons(refSeqBed):
    refSeqExons = {}
    numGenes = 0
    numRNA = 0
    numOther = 0
    for line in open(refSeqBed):
        pieces = line.split()
        id = pieces[3]
        if id.startswith("NM_"):
            numGenes += 1
            chrom = pieces[0]
            if not refSeqExons.has_key(chrom):
                refSeqExons[chrom] = []
            startStops = getExonStartStopsFromBedLine(line)
            for (blockStart, blockStop) in startStops:
                refSeqExons[chrom].append( (blockStart, blockStop) )
        elif id.startswith("NR_"):
            numRNA += 1
            # ignore for now
        else:
            numOther += 1

    print "Done reading RefSeq for Exons.  There were %s genes, %s RNAs and %s other." % (numGenes,numRNA, numOther)
    return refSeqExons

def getRefSeqRNALocations(refSeqBed):
    refSeqRNA = {}
    numGenes = 0
    numRNA = 0
    numOther = 0
    for line in open(refSeqBed):
        pieces = line.split()
        id = pieces[3]
        if id.startswith("NM_"):
            numGenes += 1
        elif id.startswith("NR_"):
            numRNA += 1
            chrom = pieces[0]
            start = int(pieces[1])
            stop = int(pieces[2])
            
            if not refSeqRNA.has_key(chrom):
                refSeqRNA[chrom] = []
            refSeqRNA[chrom].append( (start, stop) )
            #key = "%s:%s" % (start, stop)
            #if not refSeqRNA[chrom].has_key(key):
            #    refSeqRNA[chrom][key] = 1
            #else:
            #    numRepeatRNA += 1
            
        else:
            numOther += 1

    print "Done reading RefSeq for RNA.  There were %s genes, %s RNAs, and %s other." % (numGenes,
                                                                    numRNA, numOther)
    return refSeqRNA


def overlapsRefSeqExons(chrom, start, stop, refSeqExons):
    if not refSeqExons.has_key(chrom):
        return OVERLAP_NONE

    # first see if it's an exact match.  Must go through all before allowing partials
    for (rsStart, rsStop) in refSeqExons[chrom]:
        if rsStart == start and rsStop == stop:
            return OVERLAP_EXACT

    # okay, look for partials -- if either the start or the stop
    # are between ref seq start & stop, then it's an overlap
    for (rsStart, rsStop) in refSeqExons[chrom]:
        #if start >= rsStart and start <= rsStop:
        #    return OVERLAP_PARTIAL
        #if stop >= rsStart and stop <= rsStop:
        #    return OVERLAP_PARTIAL
        # above doesn't catch cases where this exon fully encapsulates ref seq exon
        if start <= rsStop and stop >= rsStart:
            return OVERLAP_PARTIAL
        
    # nothing
    return OVERLAP_NONE

def overlapsRefSeqRNA(chrom, start, stop, refSeqRNA):
    if not refSeqRNA.has_key(chrom):
        return False

    for (rsStart, rsStop) in refSeqRNA[chrom]:
        if start <= rsStop and stop >= rsStart:
            return True

    return False


# actually do the work
refSeqExons = getRefSeqExons(REFSEQ_BED_FILE)
refSeqRNA = getRefSeqRNALocations(REFSEQ_BED_FILE)
for exp in EXPERIMENTS:
    print exp
    out_exact = open(OUTPUT_NAME_EXON_EXACT % exp, "w")
    out_exact.write(TRACK_LINE_PATTERN % ("%s_exonExact" % (exp), "%s_exonExact" % (exp)))
    out_partial = open(OUTPUT_NAME_EXON_PARTIAL % exp, "w")
    out_partial.write(TRACK_LINE_PATTERN % ("%s_exonPartial" % (exp), "%s_exonPartial" % (exp)))
    out_none_known = open(OUTPUT_NAME_EXON_NONE_KNOWN % exp, "w")
    out_none_known.write(TRACK_LINE_PATTERN % ("%s_exonNone_known" % (exp), "%s_exonNone_known" % (exp)))
    out_none_novel = open(OUTPUT_NAME_EXON_NONE_NOVEL % exp, "w")
    out_none_novel.write(TRACK_LINE_PATTERN % ("%s_exonNone_novel" % (exp), "%s_exonNone_novel" % (exp)))
    countExact = countPartial = countNone = 0


    countTooShort = 0
    countOneExon = 0
    countIntronTooShort = 0
    for line in open(BED_FILE_TO_FILTER % exp):
        if line.startswith("track"):
            continue

        pieces = line.split()
        chrom = pieces[0]
        blockSizes = pieces[10].split(",")[:-1]
        if len(blockSizes) == 1:
            countOneExon += 1
            continue
        totalLength = 0
        for bs in blockSizes:
            totalLength += int(bs)
        if totalLength <= MINIMUM_TOTAL_LENGTH:
            countTooShort += 1
            continue
        startStops = getExonStartStopsFromBedLine(line)
        intronSizes = getIntronSizes(startStops)
        if max(intronSizes) < MINIMUM_INTRON_SIZE:
            countIntronTooShort += 1
            continue
        maxOverlap = OVERLAP_NONE
        for (start, stop) in startStops:
            overlapType = overlapsRefSeqExons(chrom, start, stop, refSeqExons)
            if overlapType == OVERLAP_EXACT:
                maxOverlap = OVERLAP_EXACT
                break
            elif overlapType == OVERLAP_PARTIAL:
                maxOverlap = OVERLAP_PARTIAL
    
        if maxOverlap == OVERLAP_EXACT:
            out_exact.write(line)
            countExact += 1
        elif maxOverlap  == OVERLAP_PARTIAL:
            out_partial.write(line)
            countPartial += 1
        elif maxOverlap  == OVERLAP_NONE:
            #out_none.write(line)
            if overlapsRefSeqRNA(chrom, start, stop, refSeqRNA):
                out_none_known.write(line)
            else:
                out_none_novel.write(line)
            countNone += 1
        else:
            print line
            raise Exception("Unknown overlap type returned from overlapsRefSeqExons!")
    out_exact.close()
    out_partial.close()
    out_none_known.close()
    out_none_novel.close()

    print "Done filtering bed!  There were %s transcripts that had only one exon, %s transcripts that were too short, and %s with introns too short." % (
        countOneExon, countTooShort, countIntronTooShort)
    print "There were %s transcripts with an exact overlap, %s with a partial, and %s with no overlap" % (countExact, countPartial, countNone)
