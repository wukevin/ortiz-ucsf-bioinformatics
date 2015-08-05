"""
Genome utility functions. Includes various functions for manipulating
sequences.

Written by Kevin Wu in Ortiz Lab, May 2015
"""

CODONS = {'ttt':'F', 'ttc':'F', 'tta':'L', 'ttg':'L',
          'ctt':'L', 'ctc':'L', 'cta':'L', 'ctg':'L',
          'att':'I', 'atc':'I', 'ata':'I', 'atg':'M',
          'gtt':'V', 'gtc':'V', 'gta':'V', 'gtg':'G',
          'tct':'S', 'tcc':'S', 'tca':'S', 'tcg':'S',
          'cct':'P', 'ccc':'P', 'cca':'P', 'ccg':'P',
          'act':'T', 'acc':'T', 'aca':'T', 'acg':'T',
          'gct':'A', 'gcc':'A', 'gca':'A', 'gcg':'A',
          'tat':'Y', 'tac':'Y', 'taa':'*', 'tag':'*',
          'cat':'H', 'cac':'H', 'caa':'Q', 'cag':'Q',
          'aat':'N', 'aac':'N', 'aaa':'K', 'aag':'K',
          'gat':'D', 'gac':'D', 'gaa':'E', 'gag':'E',
          'tgt':'C', 'tgc':'C', 'tga':'*', 'tgg':'W',
          'cgt':'R', 'cgc':'R', 'cga':'R', 'cgg':'R',
          'agt':'S', 'agc':'S', 'aga':'R', 'agg':'R',
          'ggt':'G', 'ggc':'G', 'gga':'G', 'ggg':'G'}

def dnaToAminoAcid(sequence, rna = False, warn = True):
    """
    Converts a given DNA/RNA sequence to an amino acid sequence. 
    If rna is set to true, then all U's will be converted to T's before
    translating.
    """
    sequence = sequence.lower()
    if (rna == True): # Convert U to T so we can properly match amino acids
        sequence.replace('u','t')
    aaSeq = ""
    if ((len(sequence) % 3) != 0) & (warn):
        print("Warning: sequence not multiple of three. Overhanging base pairs will be dropped.")
    for i in range(len(sequence) / 3):
        codon = sequence[3*i:3*i+3]
        aaSeq = aaSeq + CODONS[codon]
    return aaSeq

def reverseComplement(sequence, rna = False):
    """
    Return the reverse complement of either a DNA or RNA sequence.
    """
    if (rna == False):
        BP = {'a':'t', 't':'a', 'c':'g', 'g':'c'}
    else:
        BP = {'a':'u', 'u':'a', 'c':'g', 'g':'c'}
    reverse = sequence[::-1].lower() # Reverse the sequence
    reverseComplement = ""
    for i in range(len(reverse)): # Get the complement of the sequence
        reverseComplement = reverseComplement + BP[reverse[i]]
    return reverseComplement

def splitSequence(line, n = 1):
    """
    Splits a nucelotide sequence into units of length n.
    """
    splitted = [line[i:i+n] for i in range(0, len(line), n)]
    return splitted
