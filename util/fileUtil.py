"""
Utility functions for working with files. Thus far, there are only functions
that extract useful information from filenames, such as cell line. However,
this can be expanded in the future as necessary

Kevin Wu, Ortiz Lab, UCSF, August 2015
"""

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
