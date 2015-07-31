#!/bin/bash
# Place in the STAR output folder, and this will copy all the .bam files to a separate
# directory and run trinity, then run PASA on each bam.

# Make trinity folder, copy all .bam files over to it
mkdir trinity
for i in $(ls | grep .bam$); do
	cp "$i" trinity/
done
# Go into trinity folder
cd trinity
# Copy trinity script over, run it. This will create a trinity output dir
# for every bam file that was copied into this folder.
cp ~/Documents/kwu/scripts/trinity/runTrinityBatchHelper.bash $pwd
./runTrinityBatchHelper.bash
# Go into each trinity output folder, create a PASA dir, run PASA
for i in $(ls -d */); do
	cd $i
	mkdir pasa
	cp Trinity-GG.fasta pasa
	cd pasa
	cp ~/Documents/kwu/scripts/pasa/* $pwd
	./runPASA.bash
	# Exits to the trinity output folder parent, remove all but necessary files
	cd ..
	ls | grep -v .fasta$ | grep -v pasa | xargs rm -r
	# Exits to the trinity folder
	cd ..
done
