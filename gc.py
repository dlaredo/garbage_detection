'''
Author: David Laredo Razo
Intel's garbage cleaner for BIOS Development
March, 2016
'''

import sys
import os
import os.path
import re
import stat
from infFileContents import *

def create_inf_files_list(search_directory):

	"""Creates a list of all the .inf files found within the search folder and its sub folders"""

	"""
	Arguments:
		search_directory: The absolute path to the directory from the code will start searching for .inf files
	"""

	"""
	Returns:
		A list of objects representing the .inf files located in the search folder and its sub folders.
	"""

	inf_files_list = list()
	inf_file = InfFile()

	print("Creating .inf files list\n")

	#Traverse the whole directory tree
	for root, dir, files in os.walk(search_directory):

		for element in files:
			(name, ext) = os.path.splitext(element)

			if ext == '.inf':

				inf_file = InfFile()
				infFilePath = os.path.join(root, element)
				print("Checking file " + infFilePath)
				inf_file.parse_inf_file(infFilePath)
				inf_files_list.append(inf_file)
				#inf_file.printInfObject()
				#wait = input("Press Enter to continue")

def detect_unused_elements(root_directory, search_directory):

	"""Determines the unused elements in each .inf file located in the directory tree startign from search_directory"""

	"""
	Arguments:
		root_directory: The absolute path to the root directory of the BIOS source code
		search_directory: The absolute path to the directory from the code will start searching for .inf files
	"""

	unused_elements_file = open(os.path.join(search_directory, "unusedElements.txt"), "w");

	inf_files_list = create_inf_files_list(search_directory)

#Main function
def main():
	"""This function locates the unused components (guids, ppis, protocols, etc) that are declared in the .inf files used for compiling BIOS"""

	"""
	Arguments:
		root_directory: The absolute path to the root directory of the BIOS source code
		search_directory: The absolute path to the directory from the code will start searching for .inf files
	"""

	"""
	Returns:
		By the end of the execution of this program a new file called unused_components.txt
		is created in root_directory
	"""

	current_directory = '';
	root_directory = '';

	if len(sys.argv) < 2:
		print('Use: gc.py root_directory [search_directory]');
		quit();

	root_directory = str(sys.argv[1]);

	if len(sys.argv) < 3:
		search_directory = os.curdir;
	else:
		search_directory = str(sys.argv[2]);

	detect_unused_elements(root_directory, search_directory);


main();