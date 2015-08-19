"""Utility functions for interacting with the unix bash shell"""

import sys, os
import select
import subprocess

def executeFunctions(listOfFunc, parallel = False, simulate = False, captureOutput = False):
    def execHelper(c, capture = captureOutput):
        if capture:
            result = subprocess.check_output(c, shell = True)
            return result
        else:
            subprocess.call(c, shell = True)
            return
    
    if len(listOfFunc) == 0: # If no commands, return
        return
    elif len(listOfFunc) == 1: # If only one command, then 
        if simulate:
            print(listOfFunc[0])
            return
        else:
            execHelper(listOfFunc[0])
    elif isinstance(listOfFunc, str):
        execHelper(listOfFunc)
    else: # Is actually a list of functions, and treat as such
        if parallel: # Runs each command as a background process, effectively parallelizing
            sep = " & "
            listOfFunc.append("wait") # Prevents premature termination in shell
        else: # Runs each command as foreground sequentially
            sep = " && "
        command = sep.join(listOfFunc)
        
        if simulate: # If only simulating, print command and exit
            print(command)
            return
        else:
            execHelper(command)

def isStdInEmpty():
    # WARNING: This only works on Unix systems!
    # http://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
    if select.select([sys.stdin,],[],[],0.0)[0]:
        return False
    else:
        return True

def getStdIn():
    # Returns a list, where each element is a line of input from StdIn
    raw = sys.stdin.readlines()
    processed = []
    for line in raw:
        line = line.rstrip()
        processed.append(line)
    return processed
