import subprocess
import sys

def getToolFromFilename(f, delim = "_"):
    splitted = f.split(delim)
    tool = splitted[len(splitted)-2]
    return tool

def getCellLineFromFilename(f, delim = "_"):
    splitted = f.split(delim)
    b = max([splitted.index(x) for x in ["Trinity", "Cufflinks", "Stringtie"] if x in splitted])
    line = "_".join(splitted[0:b])
    return line

def runCuffDiff(*args):
    commandTemplate = "cuffcompare -s /media/Data/genomes/hg19_ordered/hg19.fa -o %s -r %s %s"
    prefixTemplate = "%s_%s_vs_%s_ref"
    commands = []
    if (len(args) < 4 and len(args) > 1):
        if len(args) == 2:
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[0]))
            commands.append(commandTemplate % (prefix, args[0], args[1]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[1]))
            commands.append(commandTemplate % (prefix, args[1], args[0]))
        elif len(args) == 3:
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[0]))
            commands.append(commandTemplate % (prefix, args[0], args[1]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[2]), getToolFromFilename(args[0]))
            commands.append(commandTemplate % (prefix, args[0], args[2]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[1]))
            commands.append(commandTemplate % (prefix, args[1], args[0]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[2]), getToolFromFilename(args[1]))
            commands.append(commandTemplate % (prefix, args[1], args[2]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[0]), getToolFromFilename(args[2]))
            commands.append(commandTemplate % (prefix, args[2], args[0]))
            prefix = prefixTemplate % (getCellLineFromFilename(args[0]), getToolFromFilename(args[1]), getToolFromFilename(args[2]))
            commands.append(commandTemplate % (prefix, args[2], args[1]))
    else:
        print("This program takes 2 or 3 input arguments. Each input must be a .gtf")
        print("file. We then use CuffCompare to do pairwise comparisons and return")
        print("a final merged .gtf. Order of input does not matter.")
        exit()
    filename = getCellLineFromFilename(args[0]) + "_cuffcompare_commands.log"
    f = open(filename, mode = "w")
    for command in commands:
        subprocess.call(command, shell = True)
        f.write(command + "\n")
    f.close()
    return commands

commands = runCuffDiff(*sys.argv[1:])
print(commands)
