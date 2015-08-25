"""
Utility functions for working with files. Thus far, there are only functions
that extract useful information from filenames, such as cell line. However,
this can be expanded in the future as necessary

Kevin Wu, Ortiz Lab, UCSF, August 2015
"""
import gzip
import re

def getCellLineFromFilename(f, delim = "_"):
    # Assumes that the cell line is the first part of the name
    f = f.split(".")[0] # Removes file extension
    splitted = f.split(delim)
    if "Trinity" in splitted or "Cufflinks" in splitted or "Stringtie" in splitted:
        b = max([splitted.index(x) for x in ["Trinity", "Cufflinks", "Stringtie"] if x in splitted])
        line = "-".join(splitted[0:b])
    else:
        line = splitted[0]
    return line

def longestCommonSubstring(S, T):
    # http://www.bogotobogo.com/python/python_longest_common_substring_lcs_algorithm_generalized_suffix_tree.php
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])
    return lcs_set.pop()

def stripKnownFileExtensions(filename):
    knownFileExtensions = ["\.tar",
                           "\.gz",
                           "\.zip",
                           "\.fastq",
                           "\.fasta"]
    for ext in knownFileExtensions:
        re.sub(ext, '', filename)
    return filename

def meanFastqReadLength(filename):
    # Gets the average read length from a fastq file (gzipped or not works)
    totalLength = 0
    totalReads = 0
    if "gz" in filename:
        with gzip.open(filename) as x:
            previousLine=""
            for line in x:
                if len(previousLine) > 1 and previousLine[0] == "@":
                    totalReads = totalReads + 1
                    totalLength = totalLength + len(line)
                previousLine = line
        meanLength = totalLength / totalReads
        return meanLength
    else:
        with open(filename) as x:
            previousLine=""
            for line in x:
                if len(previousLine) > 1 and previousLine[0] == "@":
                    totalReads = totalReads + 1
                    totalLength = totalLength + len(line)
                previousLine = line
        meanLength = totalLength / totalReads
        return meanLength
