'''
Author: David Laredo Razo
Intel's Tool for determining unused packages
February, 2016
'''

import sys
import os
import os.path
import re
import stat
from enum import Enum

class infFileContents:
	
	defines = set();
	sources = set();
	packages = set();
	libraryClasses = set();
	protocols = set();
	guids = set();
	pcd = set();
	depex = set();
	ppis = set();
	fixedpcd = set();
	featurepcd = set();

	def __init__(self):
		self.defines = set();
		self.sources = set();
		self.packages = set();
		self.libraryClasses = set();
		self.protocols = set();
		self.guids = set();
		self.pcd = set();
		self.depex = set();
		self.ppis = set();
		self.fixedpcd = set();
		self.featurepcd = set();

function_pattern = re.compile("([a-zA-Z_][a-zA-Z_\d]*\s*\([&\sa-zA-Z_\d,\*\"]*\);?)");
variableName_pattern = re.compile("([a-zA-Z_][a-zA-Z_\d]*)");
relativePath_pattern = re.compile("(\.{1,2}[\/\\\\]|[a-zA-Z_][a-zA-Z_\d]*[\/\\\\]|[\/\\\\])+[a-zA-Z_][a-zA-Z_\d]*.[ch]", re.IGNORECASE);

#Patterns for looking for headers
defines_pattern = re.compile("\[Defines.*\]", re.IGNORECASE);
sources_pattern = re.compile("\[Sources.*\]", re.IGNORECASE);
packages_pattern = re.compile("\[Packages.*]", re.IGNORECASE);
libraryClasses_pattern = re.compile("\[LibraryClasses.*]", re.IGNORECASE);
protocols_pattern = re.compile("\[Protocols.*\]", re.IGNORECASE);
guids_pattern = re.compile("\[Guids.*\]", re.IGNORECASE);
pcd_pattern = re.compile("\[Pcd.*\]", re.IGNORECASE);
depex_pattern = re.compile("\[Depex.*\]", re.IGNORECASE);
buildop_pattern = re.compile("\[BuildOptions.*\]", re.IGNORECASE);
ppis_pattern = re.compile("\[Ppis.*\]", re.IGNORECASE);
fixedPcd_pattern = re.compile("\[FixedPcd.*\]", re.IGNORECASE);
featurePcd_pattern = re.compile("\[FeaturePcd.*\]", re.IGNORECASE);
genericHeader_pattern = re.compile("\[.*\]", re.IGNORECASE);


#Used to obtain a list of the unused files in a defined module
def get_unused_list(root_directory, search_directory):

	sourceFilesPathList = [];
	functionSet = set();
	paramSet = set();
	usedGuidsSet = set();
	usedPcdsSet = set();
	usedProtocolsSet = set();
	usedPpisSet = set();
	usedFixedPcdsSet = set();
	usedFeaturePcdsSet = set();
	unusedElementsFile = '';
	fileBuffer = '';
	totalElements = dict([('guids', 0), ('pcds', 0), ('protocols', 0), ('ppis', 0), ('fixedPcd', 0), ('featurePcd', 0)]);
	totalUnusedElements = dict([('guids', 0), ('pcds', 0), ('protocols', 0), ('ppis', 0), ('fixedPcd', 0), ('featurePcd', 0)]);
	temp1, temp2, temp3, temp4, temp9, temp11 = 0, 0, 0, 0, 0, 0;
	temp5, temp6, temp7, temp8, temp10, temp12 = 0, 0, 0, 0, 0, 0;
	filePath = '';
	infFilePath = '';
	unexestingFiles = list();
	unexestingFilesInf = list();

	unusedElementsFile = open(os.path.join(search_directory, "unusedElements.txt"), "w");

	#Traverse the whole directory tree
	for root, dir, files in os.walk(search_directory):

		for element in files:
			(name, ext) = os.path.splitext(element)

			if ext == '.inf':

				infFilePath = os.path.join(root, element)

				print("Checking file " + infFilePath);
				infFileContents = parse_inf_file(infFilePath);
				printInfObject(infFileContents);
				wait = input("PRESS ENTER TO CONTINUE.");

				for package in infFileContents.packages:
					for dirElement in os.listdir(os.path.join(root_directory, package)):
						print(dirElement + "\n");

				wait = input('Enter');


				
				#Add to total number of elements found
				temp1, temp2, temp3, temp4, temp9, temp11 =\
				len(infFileContents.guids), len(infFileContents.pcd), len(infFileContents.protocols),\
				len(infFileContents.ppis), len(infFileContents.fixedpcd), len(infFileContents.featurepcd);

				totalElements['guids'] += temp1;
				totalElements['pcds'] += temp2;
				totalElements['protocols'] += temp3;
				totalElements['ppis'] += temp4;
				totalElements['fixedPcd'] += temp9;
				totalElements['featurePcd'] += temp11;

				#printInfObject(infFileContents)
				for cSourceFile in infFileContents.sources:
					(sourceName, sourceExt) = os.path.splitext(cSourceFile);

					#For each C file of the module (*.inf file)
					if sourceExt == '.c':

						filePath = os.path.join(root, cSourceFile.replace("$(OPENSSL_PATH)", "openssl-0.9.8zf"));

						print("Analizing " + filePath + " file");
						fileBuffer = '';

						try:
							#Load entire file into buffer
							with open(filePath, 'r', -1, 'utf-8') as cSourceFile:
								fileBuffer = cSourceFile.read().replace('\n', ' ');
							cSourceFile.close();
						except FileNotFoundError:
							unexestingFiles.append(cSourceFile);
							unexestingFilesInf.append(infFilePath)
						except Exception as e:
							#Load entire file into buffer
							with open(filePath, 'r', -1, 'cp1252') as cSourceFile:
								fileBuffer = cSourceFile.read().replace('\n', ' ');
							cSourceFile.close();
						finally:
							pass
						

						#find guids in file
						for guid in infFileContents.guids:
							if fileBuffer.find(guid) != -1:
								usedGuidsSet.add(guid);

						#find pcds in file
						for pcd in infFileContents.pcd:
							if fileBuffer.find(pcd) != -1:
								usedPcdsSet.add(pcd);

						#find protocols in file
						for protocol in infFileContents.protocols:
							if fileBuffer.find(protocol) != -1:
								usedProtocolsSet.add(protocol);

						#find ppis in file
						for ppi in infFileContents.ppis:
							if fileBuffer.find(ppi) != -1:
								usedPpisSet.add(ppi);

						#find fixedpcd in file
						for fixedpcd in infFileContents.fixedpcd:
							if fileBuffer.find(fixedpcd) != -1:
								usedFixedPcdsSet.add(fixedpcd);

						#find featurepcd in file
						for featurepcd in infFileContents.featurepcd:
							if fileBuffer.find(featurepcd) != -1:
								usedFeaturePcdsSet.add(featurepcd);

						#Remove found guids, pcd, and protocols from infFileContents object.
						#Remaining guids, pcd and protocols at the infFileContents object at the end of this pass are the ones that are unused.

						infFileContents.guids = infFileContents.guids - usedGuidsSet;
						infFileContents.pcd = infFileContents.pcd - usedPcdsSet;
						infFileContents.protocols = infFileContents.protocols - usedProtocolsSet;
						infFileContents.ppis = infFileContents.ppis - usedPpisSet;
						infFileContents.fixedpcd = infFileContents.fixedpcd - usedFixedPcdsSet;
						infFileContents.featurepcd = infFileContents.featurepcd - usedFeaturePcdsSet;

				#Add to total number of unused elements
				temp5, temp6, temp7, temp8, temp10, temp12 =\
				len(infFileContents.guids), len(infFileContents.pcd), len(infFileContents.protocols),\
				len(infFileContents.ppis), len(infFileContents.fixedpcd), len(infFileContents.featurepcd);

				totalUnusedElements['guids'] += temp5;
				totalUnusedElements['pcds'] += temp6;
				totalUnusedElements['protocols'] += temp7;
				totalUnusedElements['ppis'] += temp8;
				totalUnusedElements['fixedPcd'] += temp10;
				totalUnusedElements['featurePcd'] += temp12;

				#Write new inf file
				#replace_inf_file(root, element, infFileContents);

				#Print unused elements in file
				if len(infFileContents.guids) + len(infFileContents.ppis) + len(infFileContents.protocols) != 0:
					unusedElementsFile.write("Path: \t\t" + root + "\n");
					unusedElementsFile.write("File: \t\t" + element + "\n\n");
					
					if len(infFileContents.guids) != 0:
						unusedElementsFile.write("[GUIDS] [Total GUID's in .inf file: " + str(temp1) + " Number of unused: " + str(temp5) + "]\n\n");

						for guid in infFileContents.guids:
							unusedElementsFile.write(guid + "\n");

					'''
					if len(infFileContents.pcd) != 0:
						unusedElementsFile.write("\n[PCDS] [Total PCD's in .inf file: " + str(temp2) + " Number of unused: " + str(temp6) + "]\n\n");

						for pcd in infFileContents.pcd:
							unusedElementsFile.write(pcd + "\n");'''

					if len(infFileContents.protocols) != 0:
						unusedElementsFile.write("\n[PROTOCOLS] [Total PROTOCOLS's in .inf file: " + str(temp3) + " Number of unused: " + str(temp7) + "]\n\n");

						for protocol in infFileContents.protocols:
							unusedElementsFile.write(protocol + "\n");

					if len(infFileContents.ppis) != 0:
						unusedElementsFile.write("\n[PPIS] [Total PPI's in .inf file: " + str(temp4) + " Number of unused: " + str(temp8) + "]\n\n");

						for ppi in infFileContents.ppis:
							unusedElementsFile.write(ppi + "\n");

					'''
					if len(infFileContents.fixedpcd) != 0:
						unusedElementsFile.write("\n[FIXEDPCDS] [Total FIXEDPCD's in .inf file: " + str(temp9) + " Number of unused: " + str(temp10) + "]\n\n");

						for fixedpcd in infFileContents.fixedpcd:
							unusedElementsFile.write(fixedpcd + "\n");

					if len(infFileContents.featurepcd) != 0:
						unusedElementsFile.write("\n[FEATUREPCDS] [Total FEATUREPCD's in .inf file: " + str(temp11) + " Number of unused: " + str(temp12) + "]\n\n");

						for featurepcd in infFileContents.featurepcd:
							unusedElementsFile.write(featurepcd + "\n");'''

					unusedElementsFile.write('\n================================================================================================================\n');

	unusedElementsFile.write("\nNumber of GUIDs found: " + str(totalElements['guids']));
	#unusedElementsFile.write("\nNumber of PCDs found: " + str(totalElements['pcds']));
	unusedElementsFile.write("\nNumber of PROTOCOLS found: " + str(totalElements['protocols']));
	unusedElementsFile.write("\nNumber of PPIs found: " + str(totalElements['ppis']));
	#unusedElementsFile.write("\nNumber of FIXEDPCDs found: " + str(totalElements['fixedPcd']));
	#unusedElementsFile.write("\nNumber of FEATUREPCDs found: " + str(totalElements['featurePcd']));

	unusedElementsFile.write("\n\nNumber of unused GUIDs: " + str(totalUnusedElements['guids']));
	#unusedElementsFile.write("\nNumber of unused PCDs: " + str(totalUnusedElements['pcds']));
	unusedElementsFile.write("\nNumber of unused PROTOCOLS: " + str(totalUnusedElements['protocols']));
	unusedElementsFile.write("\nNumber of unused PPIs: " + str(totalUnusedElements['ppis']));
	#unusedElementsFile.write("\nNumber of unused FIXEDPCDs: " + str(totalUnusedElements['fixedPcd']));
	#unusedElementsFile.write("\nNumber of unused FEATUREPCDs: " + str(totalUnusedElements['featurePcd']));

	unusedElementsFile.write("\n\nFiles not found:\n\n ");

	for count in range(len(unexestingFiles)):
		unusedElementsFile.write(unexestingFilesInf[count] + ": " + unexestingFiles[count] + "\n");

	unusedElementsFile.close();



#Create an object with the structure of the .inf file
def parse_inf_file(path_to_file):

	fileContents = infFileContents();

	class sections(Enum):
		SECTION_GENERICHEADER, SECTION_DEFINES, SECTION_SOURCES, SECTION_PACKAGES, SECTION_LIBRARYCLASSES,\
		SECTION_PROTOCOLS, SECTION_GUIDS, SECTION_PCD, SECTION_DEPEX, SECTION_BUILDOP, SECTION_PPIS,\
		SECTION_FIXEDPCD, SECTION_FEATUREPCD = range(0,13);

	section = 0;

	with open(path_to_file) as inf_file:
		for line in inf_file:
			#print(line);

			#skip empty lines
			if line.isspace():
				continue;

			#Detect a new section of the file
			if defines_pattern.search(line):
				section = sections.SECTION_DEFINES;
				continue;

			elif sources_pattern.search(line):
				section = sections.SECTION_SOURCES;
				continue;

			elif packages_pattern.search(line):
				section = sections.SECTION_PACKAGES;
				continue;

			elif libraryClasses_pattern.search(line):
				section = sections.SECTION_LIBRARYCLASSES;
				continue;

			elif protocols_pattern.search(line):
				section = sections.SECTION_PROTOCOLS;
				continue;

			elif guids_pattern.search(line):
				section = sections.SECTION_GUIDS;
				continue;

			elif pcd_pattern.search(line):
				section = sections.SECTION_PCD;
				continue;

			elif depex_pattern.search(line):
				section = sections.SECTION_DEPEX;
				continue;

			elif buildop_pattern.search(line):
				section = sections.SECTION_BUILDOP;
				continue;

			elif fixedPcd_pattern.search(line):
				section = sections.SECTION_FIXEDPCD;
				continue;

			elif featurePcd_pattern.search(line):
				section = sections.SECTION_FEATUREPCD;
				continue;

			elif ppis_pattern.search(line):
				section = sections.SECTION_PPIS;
				continue;

			elif genericHeader_pattern.search(line):
				section = sections.SECTION_GENERICHEADER;
				continue;

			elif re.search("^\s*(#+|/{2}).*$", line):  #Ignore comment lines
				continue;

			#If no new section is detected then assign the value of the current line to the corresponding field of the infFileContents Object 
			#line = line.strip(' \t\n\r');
			#print(line)
			line = line.split()[0];

			if section == sections.SECTION_DEFINES:
				fileContents.defines.add(line);

			elif section == sections.SECTION_SOURCES:
				fileContents.sources.add(line);

			elif section == sections.SECTION_PACKAGES:
				fileContents.packages.add(line);

			elif section == sections.SECTION_LIBRARYCLASSES:
				fileContents.libraryClasses.add(line);

			elif section == sections.SECTION_PROTOCOLS:
				fileContents.protocols.add(line);

			elif section == sections.SECTION_GUIDS:
				fileContents.guids.add(line);

			elif section == sections.SECTION_PCD:
				fileContents.pcd.add(line.split('.')[1]);

			elif section == sections.SECTION_DEPEX:
				fileContents.depex.add(line);

			elif section == sections.SECTION_PPIS:
				fileContents.ppis.add(line);

			elif section == sections.SECTION_FIXEDPCD:
				fileContents.fixedpcd.add(line.split('.')[1]);

			elif section == sections.SECTION_FEATUREPCD:
				fileContents.featurepcd.add(line.split('.')[1]);

			elif section == sections.SECTION_GENERICHEADER:  #If it is a header that is not to be considered then skip that line.
				pass;

	inf_file.close();

	return fileContents;

#Replace the contents of the .inf file
def replace_inf_file(root, element, infFileContents):

	class sections(Enum):
		SECTION_GENERICHEADER, SECTION_DEFINES, SECTION_SOURCES, SECTION_PACKAGES, SECTION_LIBRARYCLASSES,\
		SECTION_PROTOCOLS, SECTION_GUIDS, SECTION_PCD, SECTION_DEPEX, SECTION_BUILDOP, SECTION_PPIS,\
		SECTION_FIXEDPCD, SECTION_FEATUREPCD = range(0,13);

	line = "";
	tempLine = "";

	print(element);

	path_to_old_file = os.path.join(root, element);
	#print(path_to_old_file);

	(name, ext) = os.path.splitext(element)

	path_to_new_file = os.path.join(root, name + "_new" + ext);
	#print(path_to_new_file);

	section = 0;

	with open(path_to_old_file) as inf_file:
		with open(path_to_new_file, 'w') as new_inf_file:
			for line in inf_file:

				#skip empty lines
				if line.isspace():
					new_inf_file.write("\n");
					continue;

				#Detect a new section of the file
				if protocols_pattern.search(line):
					section = sections.SECTION_PROTOCOLS;
					new_inf_file.write(line);
					continue;

				elif guids_pattern.search(line):
					section = sections.SECTION_GUIDS;
					new_inf_file.write(line);
					continue;

				elif ppis_pattern.search(line):
					section = sections.SECTION_PPIS;
					new_inf_file.write(line);
					continue;

				#If no new section is detected then assign the value of the current line to the corresponding field of the infFileContents Object 
				tempLine = line.split()[0];

				if section == sections.SECTION_PROTOCOLS:
					if tempLine in infFileContents.protocols:
						continue;

				elif section == sections.SECTION_GUIDS:
					if tempLine in infFileContents.guids:
						continue;

				elif section == sections.SECTION_PPIS:
					if tempLine in infFileContents.ppis:
						continue;

				new_inf_file.write(line);

	inf_file.close();
	new_inf_file.close();

	os.chmod(path_to_old_file, stat.S_IWRITE);
	os.remove(path_to_old_file);
	os.rename(path_to_new_file, path_to_old_file);
	os.chmod(path_to_old_file, stat.S_IREAD);

#Function to print the contents of the infFile Object
def printInfObject(infFileObject):

	print("defines: ")
	for element in infFileObject.defines:
		print(element);
	print("sources: ")
	for element in infFileObject.sources:
		print(element);
	print("packages: ")
	for element in infFileObject.packages:
		print(element);
	print("libraryClasses: ")
	for element in infFileObject.libraryClasses:
		print(element);
	print("protocols: ")
	for element in infFileObject.protocols:
		print(element);
	print("guids: ")
	for element in infFileObject.guids:
		print(element);
	print("pcd: ")
	for element in infFileObject.pcd:
		print(element);
	print("depex: ")
	for element in infFileObject.depex:
		print(element);

#Main function
def main():
	current_directory = '';
	root_directory = '';

	if len(sys.argv) < 1:
		print('Use: instructions');
		quit();

	root_directory = str(sys.argv[1]);

	if len(sys.argv) < 3:
		search_directory = os.curdir;
	else:
		search_directory = str(sys.argv[2]);

	print(search_directory);
	print(root_directory);
	wait = input("PRESS ENTER TO CONTINUE.");
	get_unused_list(root_directory, search_directory);


main();