#!/bin/bash
# Script for running Trinity on all .bam files in the current working directory
# http://www.ncbi.nlm.nih.gov/pubmed/15217358 for max intron size of 11,000
for i in $(ls | grep .bam$); do
    declare -x folderSuffix="_trinityOut"
    declare -x foldername="$i$folderSuffix"
    declare -x logname="$foldername/log"
    mkdir "$foldername"
    $TRINITY_HOME/Trinity --genome_guided_bam "$i" --genome_guided_max_intron 11000 --max_memory 54G --CPU 16 --output "$foldername" | tee "$logname"
done
