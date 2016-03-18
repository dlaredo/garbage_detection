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
from infFileHandler import *
from sourceFilesHandler import *

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
			inf_files_list: A list of objects representing the .inf files located in the search folder and its sub folders.
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
					inf_file.path = root
					inf_file.file_name = element
					print("Parsing file " + os.path.join(inf_file.path, inf_file.file_name))
					inf_file.parse_inf_file(os.path.join(inf_file.path, inf_file.file_name))
					inf_files_list[inf_file.base_name] = inf_file
					#inf_file.printInfObject()
					#wait = input("Press Enter to continue")

		return inf_files_list

	def detect_unused_elements(self, root_directory, search_directory):

		"""Determines the unused elements in each .inf file located in the directory tree startign from search_directory"""

		"""
		Arguments:
			root_directory: The absolute path to the root directory of the BIOS source code
			search_directory: The absolute path to the directory from the code will start searching for .inf files
		"""

		total_elements = dict([('guids', 0), ('pcds', 0), ('protocols', 0), ('ppis', 0), ('fixedPcd', 0), ('featurePcd', 0)]);
		total_unused_elements = dict([('guids', 0), ('pcds', 0), ('protocols', 0), ('ppis', 0), ('fixedPcd', 0), ('featurePcd', 0)]);
		driver_pattern = re.compile("(.*DRIVER.*|.*PEIM.*)", re.IGNORECASE)
		sourceFileHandler = SourceFilesHandler()
		total_unexesting_files = list()
		total_unexesting_files_inf = list()

		unused_elements_file = open(os.path.join(search_directory, "unusedElements.txt"), "w");

		inf_files_list = self.create_inf_files_list(search_directory)

		#For each .inf file search for unused elements
		for base_name in inf_files_list:

			inf_file = inf_files_list[base_name]

			print("\nCleaning " + os.path.join(inf_file.path, inf_file.file_name));

			#Add to total number of elements found
			number_of_guids, number_of_pcds, number_of_protocols, number_of_ppis, number_of_fixed_pcds, number_of_feature_pcds =\
			len(inf_file.guids), len(inf_file.pcds), len(inf_file.protocols),\
			len(inf_file.ppis), len(inf_file.fixed_pcds), len(inf_file.feature_pcds)
			
			total_elements['guids'] += number_of_guids
			total_elements['pcds'] += number_of_pcds
			total_elements['protocols'] += number_of_protocols
			total_elements['ppis'] += number_of_ppis
			total_elements['fixedPcd'] += number_of_fixed_pcds
			total_elements['featurePcd'] += number_of_feature_pcds

			#First attempt to determine the unused elements in the .inf file.
			used_guids_set, used_pcds_set, used_protocols_set, used_ppis_set, used_fixed_pcds_set, used_feature_pcds_set, unexesting_files, unexesting_files_inf =\
			sourceFileHandler.look_for_elements_in_source_files(inf_file)
			total_unexesting_files.extend(unexesting_files)
			total_unexesting_files_inf.extend(unexesting_files_inf)

			#Remove found guids, pcd, and protocols from inf_file_contents object.
			#Remaining guids, pcd and protocols in the inf_file_contents object at the end of this pass are the ones that are unused.
			inf_file.guids = inf_file.guids - used_guids_set
			inf_file.pcds = inf_file.pcds - used_pcds_set
			inf_file.protocols = inf_file.protocols - used_protocols_set
			inf_file.ppis = inf_file.ppis - used_ppis_set
			inf_file.fixed_pcds = inf_file.fixed_pcds - used_fixed_pcds_set
			inf_file.feature_pcds = inf_file.feature_pcds - used_feature_pcds_set

			#If there are unused elements
			if len(inf_file.guids) + len(inf_file.protocols) + len(inf_file.ppis) != 0:
			
				print(inf_file.base_name + " " +inf_file.module_type + "\n")
				#Verify that the module is not a driver: If the module is a driver and there are unused elements, then that element is misplaced and no further processing is done.
				if driver_pattern.search(inf_file.module_type):
					pass
				else:  #The module can be a Library or something else. Further processing required.
					
					#Hence, it is necessary to look for elements into every module that includes the current module.
					for library in inf_file.library_classes:
						print(library+"\n")
						dependent_inf_file = inf_files_list[library]
						dependent_inf_file.print_inf_object()
					



			#Add to total number of unused elements
			number_of_unused_guids, number_of_unused_pcds, number_of_unused_protocols, number_of_unused_ppis, number_of_unused_fixed_pcds, number_of_unused_feature_pcds =\
			len(inf_file.guids), len(inf_file.pcds), len(inf_file.protocols),\
			len(inf_file.ppis), len(inf_file.fixed_pcds), len(inf_file.feature_pcds)

			total_unused_elements['guids'] += number_of_unused_guids
			total_unused_elements['pcds'] += number_of_unused_pcds
			total_unused_elements['protocols'] += number_of_unused_protocols
			total_unused_elements['ppis'] += number_of_unused_ppis
			total_unused_elements['fixedPcd'] += number_of_unused_fixed_pcds
			total_unused_elements['featurePcd'] += number_of_unused_feature_pcds

			#Print unused elements in file
			if len(inf_file.guids) + len(inf_file.ppis) + len(inf_file.protocols) != 0:
				unused_elements_file.write("Path: \t\t" + inf_file.path + "\n")
				unused_elements_file.write("File: \t\t" + inf_file.file_name + "\n\n")
						
				if len(inf_file.guids) != 0:
					unused_elements_file.write("[GUIDS] [Total GUID's in .inf file: " + str(number_of_guids) + " Number of unused: " + str(number_of_unused_guids) + "]\n\n")

					for guid in inf_file.guids:
						unused_elements_file.write(guid + "\n")

				'''
				if len(inf_file_contents.pcd) != 0:
					unused_elements_file.write("\n[PCDS] [Total PCD's in .inf file: " + str(temp2) + " Number of unused: " + str(temp6) + "]\n\n");

					for pcd in inf_file_contents.pcd:
						unused_elements_file.write(pcd + "\n");'''

				if len(inf_file.protocols) != 0:
					unused_elements_file.write("\n[PROTOCOLS] [Total PROTOCOLS's in .inf file: " + str(number_of_protocols) + " Number of unused: " + str(number_of_unused_protocols) + "]\n\n")

					for protocol in inf_file.protocols:
						unused_elements_file.write(protocol + "\n")

				if len(inf_file.ppis) != 0:
					unused_elements_file.write("\n[PPIS] [Total PPI's in .inf file: " + str(number_of_ppis) + " Number of unused: " + str(number_of_unused_ppis) + "]\n\n")

					for ppi in inf_file.ppis:
						unused_elements_file.write(ppi + "\n")

				'''
				if len(inf_file_contents.fixedpcd) != 0:
					unused_elements_file.write("\n[FIXEDPCDS] [Total FIXEDPCD's in .inf file: " + str(temp9) + " Number of unused: " + str(temp10) + "]\n\n");

					for fixedpcd in inf_file_contents.fixedpcd:
						unused_elements_file.write(fixedpcd + "\n");

				if len(inf_file_contents.featurepcd) != 0:
					unused_elements_file.write("\n[FEATUREPCDS] [Total FEATUREPCD's in .inf file: " + str(temp11) + " Number of unused: " + str(temp12) + "]\n\n");

					for featurepcd in inf_file_contents.featurepcd:
						unused_elements_file.write(featurepcd + "\n");'''

				unused_elements_file.write('\n================================================================================================================\n');

		unused_elements_file.write("\nNumber of GUIDs found: " + str(total_elements['guids']))
		#unused_elements_file.write("\nNumber of PCDs found: " + str(totalElements['pcds']));
		unused_elements_file.write("\nNumber of PROTOCOLS found: " + str(total_elements['protocols']))
		unused_elements_file.write("\nNumber of PPIs found: " + str(total_elements['ppis']))
		#unused_elements_file.write("\nNumber of FIXEDPCDs found: " + str(totalElements['fixedPcd']));
		#unused_elements_file.write("\nNumber of FEATUREPCDs found: " + str(totalElements['featurePcd']));

		unused_elements_file.write("\n\nNumber of unused GUIDs: " + str(total_unused_elements['guids']))
		#unused_elements_file.write("\nNumber of unused PCDs: " + str(totalUnusedElements['pcds']));
		unused_elements_file.write("\nNumber of unused PROTOCOLS: " + str(total_unused_elements['protocols']))
		unused_elements_file.write("\nNumber of unused PPIs: " + str(total_unused_elements['ppis']))
		#unused_elements_file.write("\nNumber of unused FIXEDPCDs: " + str(totalUnusedElements['fixedPcd']));
		#unused_elements_file.write("\nNumber of unused FEATUREPCDs: " + str(totalUnusedElements['featurePcd']));

		unused_elements_file.write("\n\nFiles not found:\n\n")

		for count in range(len(total_unexesting_files)):
			unused_elements_file.write(total_unexesting_files_inf[count] + ": " + total_unexesting_files[count] + "\n")

		unused_elements_file.close()