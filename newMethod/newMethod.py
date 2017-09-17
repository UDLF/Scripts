######################################################
# This script aims to facilitate the implementation  #
# of new methods in the Unsupervised Distance        #
# Learning Framework (UDLF).                         #
#                                                    #
#                                                    #
# @Author: Lucas Pascotti Valem                      #
#         <lucaspascottivalem@gmail.com>             #
######################################################

import os
import sys
import math
import copy
import shutil
import fileinput
import re
import ntpath

from tempfile import mkstemp
from shutil import move
from os import remove

#replace a pattern for a substring in a file
def replace(source_file_path, pattern, substring):
	fh, target_file_path = mkstemp()
	with open(target_file_path, 'w') as target_file:
		with open(source_file_path, 'r') as source_file:
			for line in source_file:
				target_file.write(line.replace(pattern, substring))
	remove(source_file_path)
	move(target_file_path, source_file_path)

#append text to a line in a file
def appendTxt(fileToSearch, textToSearch, textToAppend):
	with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
		for line in file:
			if textToSearch in line:
				tmp = line.rstrip()
				print(line.replace(line, tmp + textToAppend), end='\n')
			else:
				print(line, end='')

#append text to a line in a file.
#this function is modified for considering and removing the ")" character at the end of a line
def appendTxtModified(fileToSearch, textToSearch, textToAppend):
	with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
		for line in file:
			if textToSearch in line:
				tmp = line.replace(")","").rstrip()
				print(line.replace(line, tmp + textToAppend), end='\n')
			else:
				print(line, end='')

#create the internal configuration file considering the given parameters
def createInternalConf(methodName, methodParams):
	f = open(os.path.join(frameworkPath, "config", methodName.lower() + ".conf"), "w")
	f.write('R"================(\n\n')
	for name,ttype,values in methodParams:
		if ttype == "STR":
			f.write("PARAM_" + methodName.upper() + "_" + name + ":" + ttype + " (")
			for i,value in enumerate(values):
				if i != 0:
					f.write(",")
				f.write(str(value))
			f.write(")\n")
		else:
			f.write("PARAM_" + methodName.upper() + "_" + name + ":" + ttype + " = " + str(values) + "\n")
	f.write('\n)================"\n')
	f.close()

#main routine
if __name__ == "__main__":
	#Print main message
	f = open("templates/message.txt", "r")
	print(f.read())
	f.close()

	#Get parameters file path
	print("INPUT:\n")
	filePath = ''
	while not os.path.isfile(filePath):
		filePath = input("File Path: ")

	#Get framework path
	frameworkPath = ''
	while not os.path.exists(frameworkPath):
		frameworkPath = input("Framework Path: ")

	head, tail = ntpath.split(filePath)
	methodName = tail.split(".")[0]

	#Check if method is already implemented in the framework
	fname = os.path.join(frameworkPath, "config", methodName.lower() + ".conf")
	if os.path.isfile(fname):
		print("ERROR: Method already implemented!!")
		exit(1)

	#Read method parameters from a given file
	content = ["".join(line.rstrip().upper().split()) for line in open(filePath)] #split lines and store in a list
	content = [x for x in content if x] #remove blank lines

	#Check if the lines are valid (syntax)
	for line in content:
		if not re.match("^.*:.*=.*$", line):
			print("\nERROR! Invalid line: " + line)
			print("Aborting...")
			exit(1)

	#Store parameter's name, types and values separately
	pnames = [x.split(':')[0] for x in content]
	ptypes = [x.split(':')[1].split('=')[0] for x in content]
	pvalues = [x.split('=')[1] for x in content]

	#Validate content
	reName = "([A-Z]+([0-9]|_)*)+"
	reType = "(UINT|DBL|BOL|STR)"
	for name in pnames:
		if not re.match(reName, name):
			print("\nERROR: " + name + " is not an acceptable parameter name!")
			print("Aborting...")
			exit(1)
	for types in ptypes:
		if not re.match(reType, types):
			print("\nERROR: " + types + " is not a possible parameter type!")
			print("Aborting...")
			exit(1)
	for i,value in enumerate(pvalues):
		types = ptypes[i]
		if types == "UINT":
			if not re.match("^[0-9]+$", value):
				print("\nERROR: " + value + " is not an integer!")
				print("Aborting...")
				exit(1)
		elif types == "DBL":
			if not re.match("^[+|-]*[0-9]+(.[0-9]+)*$", value):
				print("\nERROR: " + value + " is not a double!")
				print("Aborting...")
				exit(1)
		elif types == "BOL":
			if not re.match("^TRUE|FALSE$", value):
				print("\nERROR: " + value + " is not a possible boolean value!")
				print("Aborting...")
				exit(1)
		else:
			pvalues[i] = value.split(",")
			for x in pvalues[i]:
				if not re.match("^([A-Z]+[0-9]*)+$", x):
					print("\nERROR: " + x + " is not an acceptable string value!")
					print("Aborting...")
					exit(1)

	methodParams = [list(x) for x in zip(pnames, ptypes, pvalues)]

	#Create internal configuration file and move to the correct directory
	createInternalConf(methodName, methodParams)

	#Add the new method as an option in the general.conf file
	appendTxtModified(os.path.join(frameworkPath, "config", "general.conf"), "UDL_METHOD", ";" + methodName.upper() + ")")

	#Embed new config file (Conf.hpp)
	with open(os.path.join(frameworkPath, "src", "Core", "Conf.cpp"), 'a') as f:
		f.write('\nconst char conf' + methodName.capitalize() + '[] =\n')
		f.write('\t#include "../config/' + methodName.lower() + '.conf"\n')
		f.write(';\n')

	#Embed new config file (Validation.hpp)
	appendTxt(os.path.join(frameworkPath, "src", "Core", "Validation.hpp"), '{"NONE", confNone}', ', {"' + methodName.upper() + '",' + "conf" + methodName.capitalize() + '}')

	#Create implementation and header files
	implementationFile = os.path.join(frameworkPath,"src","Methods", methodName[:1].upper() + methodName[1:] + ".cpp")
	headerFile = os.path.join(frameworkPath,"src","Methods", methodName[:1].upper() + methodName[1:] + ".hpp")
	shutil.copyfile(os.path.join("templates", "MyNewMethod.cpp"), implementationFile)
	shutil.copyfile(os.path.join("templates", "MyNewMethod.hpp"), headerFile)
	replace(implementationFile, "MyNewMethod", methodName[:1].upper() + methodName[1:])
	replace(headerFile, "MyNewMethod", methodName[:1].upper() + methodName[1:])
	replace(headerFile, "MYNEWMETHOD_HPP", methodName.upper() + "_HPP")

	#Add parameter declarations to header
	declarations = '\n'
	for name,ttype,values in methodParams:
		declarations += '\t\t\t'
		if ttype == "UINT":
			declarations += 'int '
		elif ttype == "DBL":
			declarations += 'double '
		elif ttype == "BOL":
			declarations += 'bool '
		else:
			declarations += 'std::string '
		declarations += name.lower() + ';\n'
	appendTxt(headerFile, "Parameters (read from the configuration file)", declarations)

	#Load parameters in .cpp file
	loadParam = '\n'
	for name,ttype,values in methodParams:
		loadParam += '\texec.getConfigVariable(' + name.lower() + ', ' + '"PARAM_' + methodName.upper() + '_' + name.upper() + '");\n'
	appendTxt(implementationFile, "Parameters (read from the configuration file)", loadParam)

	#Add to Makefile
	name = methodName[:1].upper() + methodName[1:]
	with open(os.path.join(frameworkPath, "Makefile"), 'a') as f:
		f.write('\n\n#' + name + '\n')
		f.write(name + '.o: $(SRC_DIR)/Methods/' + name + '.cpp\n')
		f.write('\tmkdir -p $(OBJ_DIR)\n')
		f.write('\t$(CC) $(FLAGS) -c $(SRC_DIR)/Methods/' + name + '.cpp -o $(OBJ_DIR)/' + name + '.o\n')
	appendTxt(os.path.join(frameworkPath, "Makefile"), "OBJ       =", " " + name + '.o')

	#Add class run call to Exec.cpp
	appendTxt(os.path.join(frameworkPath, "src", "Core", "Exec.cpp"), '#include "Methods/None.hpp"', '\n#include "Methods/' + name + '.hpp"')
	appendTxt(os.path.join(frameworkPath, "src", "Core", "Exec.cpp"), "none.run();", '\n\t} else if (method == "' + methodName.upper() + '") {\n\t\t' + name + " " + methodName.lower() + ";\n\t\t" + methodName.lower() + ".run();")

	print("Success!\n")

	print("You can now implement the method in src/Methods/" + name + ".hpp and src/Methods/" + name + ".cpp")	

