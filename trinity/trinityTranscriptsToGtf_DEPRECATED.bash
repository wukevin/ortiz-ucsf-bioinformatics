#!/bin/bash
# Script for converting Trinity trancripts.fasta to a gtf file.
# Also deletes extraneous files after

# 16 threads, hg19 reference, convert to sam
# bwa mem -t 16 ~/software/bwa-*/hg19.fa Trinity-GG.fasta > Trinity-output.sam
gmap -d hg19 -f samse -n 0 -t 16 Trinity-GG.fasta > Trinity-output.sam

samtools view -Sbh Trinity-output.sam > Trinity-output.bam
bamToBed -i Trinity-output.bam > Trinity-output.bed
# bed12ToBed6 -i TrinityBWA.bed > TrinityBWA.6.bed

bedToGenePred Trinity-output.bed Trinity-output.genePred

genePredToGtf file Trinity-output.genePred Trinity-output.gtf
echo "GTF written to Trinity-output.gtf"

# Removes the files that are not either .fasta or .gtf
# ls | grep -v ".fasta$" | grep -v ".gtf$" | xargs rm -r
# Reference from online http://seqanswers.com/forums/showthread.php?t=44455
# samtools view -Sbh TrinityBWA.sam | bam2bed | bed12ToBed6 | bedToGenePred stdin stdout | genePredToGtf file stdin assembly.gtf
