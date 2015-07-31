# Runs stringtie for all .bam files in the current directory. Do NOT copy this
# script, instead make a symbolic link using ln -s
for i in $(ls | grep .bam$); do
    declare -x folderSuffix="_stringtieOut"
    declare -x foldername="$i$folderSuffix"
    declare -x logname="$foldername/stringtie.log"
    declare -x outputfile="$foldername/stringtieOutput.gtf"
    mkdir "$foldername"
    stringtie "$i" -v -o "$outputfile" -p 16 | tee "$logname"
done
