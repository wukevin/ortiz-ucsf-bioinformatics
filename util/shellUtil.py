"""Utility functions for interacting with the unix bash shell"""

import sys, os
import select
import subprocess

def executeFunctions(listOfFunc, parallel = False, simulate = False):
    if len(listOfFunc) == 0: # If no commands, return
        return
    if len(listOfFunc) == 1 or isinstance(listOfFunc, str): # If only one command, then 
        if simulate:
            print(listOfFunc[0])
            return
        else:
            subprocess.call(listOfFunc[0], shell = True)
    if parallel: # Runs each command as a background process, effectively parallelizing
        sep = " & "
        listOfFunc.append("wait") # Prevents premature termination in shell
    else: # Runs each command as foreground
        sep = " && "
    command = sep.join(listOfFunc)
    
    if simulate: # If only simulating, print command and exit
        print(command)
        return
    else:
        subprocess.call(command, shell = True)

def isStdInEmpty():
    # WARNING: This only works on Unix systems!
    # http://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
    if select.select([sys.stdin,],[],[],0.0)[0]:
        return False
    else:
        return True

def getStdIn():
    raw = sys.stdin.readlines()
    processed = []
    for line in raw:
        line = line.rstrip()
        processed.append(line)
    return processed
