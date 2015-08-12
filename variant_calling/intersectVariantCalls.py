# Convert all insertions and deletions represented to a standardized format.
# i.e. CCCT	T  turns into CCC -, or T
# For SNPs you probably won't have to do this
# Remember that some things 0-index, and others 1-index, and therefore you have to account for
# possibly have a shift of 1 (of course, assuming the original and variant are the same)
