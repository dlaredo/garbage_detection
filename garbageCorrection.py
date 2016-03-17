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

class GarbageCorrection(object):

	def __init__(self):
		pass

	def create_inf_files_list(self, search_directory):

		"""Creates a list of all the .inf files found within the search folder and its sub folders"""

		"""
		Arguments:
			search_directory: The absolute path to the directory from the code will start searching for .inf files
		"""

		"""
		Returns:
			A list of objects representing the .inf files located in the search folder and its sub folders.
		"""

		inf_files_list = dict()
		inf_file = InfFile()

		print("Creating .inf files list\n")

		#Traverse the whole directory tree in search for .inf files
		for root, dir, files in os.walk(search_directory):

			for element in files:
				(name, ext) = os.path.splitext(element)

				if ext == '.inf':

					inf_file = InfFile()
					inf_file.path = os.path.join(root, element)
					print("Checking file " + inf_file.path)
					inf_file.parse_inf_file(inf_file.path)
					inf_files_list[inf_file.base_name] = inf_file
					#inf_file.printInfObject()
					#wait = input("Press Enter to continue")

		for base_name in inf_files_list:
			

	def detect_unused_elements(self, root_directory, search_directory):

		"""Determines the unused elements in each .inf file located in the directory tree startign from search_directory"""

		"""
		Arguments:
			root_directory: The absolute path to the root directory of the BIOS source code
			search_directory: The absolute path to the directory from the code will start searching for .inf files
		"""

		unused_elements_file = open(os.path.join(search_directory, "unusedElements.txt"), "w");

		inf_files_list = self.create_inf_files_list(search_directory)