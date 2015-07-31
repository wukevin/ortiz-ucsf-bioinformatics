import sys, os

# D04 = "D04RM_DE_microarray.txt"
# mm415 = "mm415RM_DE_microarray.txt"


def getDirection(File):
    Dic = {"Up":[],"Down":[]}
    with open(File,'rU') as infile:
        header = infile.readline()
        header = header.split('\t')
        for line in infile:
            splitted = line.split('\t')
            Info = splitted[3]
            Gene = splitted[-3]
            if "-" in Info:
                Dic["Down"].append(Gene)
            else:
                Dic["Up"].append(Gene)
    return Dic

# D04_Dic = getDirection(D04)
# mm415_Dic = getDirection(mm415)

def parseUserInput(args):
	if len(args) == 4:
		xDic = getDirection(args[1])
		yDic = getDirection(args[2])
		upIntersection = set(xDic["Up"]) & set(yDic["Up"])
		downIntersection = set(xDic["Down"]) & set(yDic["Down"])
		# Write upregulated
		outfileUp = open(args[3] + "_up_intersection.txt", mode = "w")
		for gene in upIntersection:
			outfileUp.write(gene + "\n")
		outfileUp.close()
		print("Intersection of upregulated genes written to " + outfileUp.name)
		# Write downregulated
		outfileDown = open(args[3] + "_down_intersection.txt", mode = "w")
		for gene in downIntersection:
			outfileDown.write(gene + "\n")
		outfileDown.close()
		print("Intersection of downregulated genes written to " + outfileDown.name)
	else:
		print("This program takes three commandline arguments, in this order:" +
			  "\n- File_1.txt ~ One of the microarray expression files to compare." + 
			  "\n- File_2.txt ~ The other microarray expressoin file to compare." + 
			  "\n- output_prefix ~ The prefix for the output files.")
 
parseUserInput(sys.argv)

# Up_Intersection = set(D04_Dic["Up"]) & set(mm415_Dic["Up"])
# Down_Intersection = set(D04_Dic["Down"]) & set(mm415_Dic["Down"])        
        
