#!/bin/bash
# Clean the transcripts
seqclean Trinity-GG.fasta -c 16
# Of 25 commands, we want to run 1-14, and 16-25, skipping 15
# Command 15 is "descriptions of alignment assemblies and how they were constructed from the underlying transcript alignments" and always hangs the computer
# Creates db, runs 1-14 and does not execute 15
$PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -C -r -R -g /home/ortiz-lab/Downloads/hg19/hg19.fa -t Trinity-GG.fasta.clean -T -u Trinity-GG.fasta --ALIGNERS gmap --CPU 16 -e 15 | tee log_cmd1-14
# Restarts at command 16
$PASAHOME/scripts/Launch_PASA_pipeline.pl -c alignAssembly.config -R -g /home/ortiz-lab/Downloads/hg19/hg19.fa -t Trinity-GG.fasta.clean -T -u Trinity-GG.fasta --ALIGNERS gmap --CPU 16 -s 16 | tee log_cmd16-25
# Formerly used the hg19.fa in the downloads folder, now using the hg19 in /media/Data/genomes/
