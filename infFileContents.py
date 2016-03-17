import re
from enum import Enum

class sections(Enum):
	SECTION_GENERICHEADER, SECTION_DEFINES, SECTION_SOURCES, SECTION_PACKAGES, SECTION_LIBRARYCLASSES,\
	SECTION_PROTOCOLS, SECTION_GUIDS, SECTION_PCD, SECTION_DEPEX, SECTION_BUILDOP, SECTION_PPIS,\
	SECTION_FIXEDPCD, SECTION_FEATUREPCD = range(0,13);

class InfFile(object):
	"""Represents and stores the contents of an .inf file."""
	
	"""
	Atibutes:
		defines:
		sources: A set containing the partial path of the source files found in the .inf file.
		packages: A set containing the packages being found in the .inf file.
		library_classes: A set containing the libaries being found in the .inf file.
		protocols: A set containing the names of the protocols found in the .inf file.
		guids: A set containing the names of the guids found in the .inf file.
		pcds: A set containing the names of the pcds found in the .inf file.
		depex: A set containing the names of the depexes found in the .inf file.
		ppis: A set containing the names of the ppis found in the .inf file.
		fixed_pcds: A set conatining the names of the fixed pcds found in the .inf file.
		feature_pcds: A set conatining the names of the feature pcds found in the .inf file.
	"""

	inf_version = ''
	base_name = ''
	file_guid = ''
	module_type = ''
	version_string = ''
	entry_point = ''
	path = ''

	defines = set()
	sources = set()
	packages = set()
	library_classes = set()
	protocols = set()
	guids = set()
	pcds = set()
	depexs = set()
	ppis = set()
	fixed_pcds = set()
	feature_pcds = set()

	#Patterns for looking for headers in the .inf file
	__defines_pattern = re.compile("\[Defines.*\]", re.IGNORECASE)
	__source_pattern = re.compile("\[Sources.*\]", re.IGNORECASE)
	__package_pattern = re.compile("\[Packages.*]", re.IGNORECASE)
	__library_class_pattern = re.compile("\[LibraryClasses.*]", re.IGNORECASE)
	__protocol_pattern = re.compile("\[Protocols.*\]", re.IGNORECASE)
	__guid_pattern = re.compile("\[Guids.*\]", re.IGNORECASE)
	__pcd_pattern = re.compile("\[Pcd.*\]", re.IGNORECASE)
	__depex_pattern = re.compile("\[Depex.*\]", re.IGNORECASE)
	__buildop_pattern = re.compile("\[BuildOptions.*\]", re.IGNORECASE)
	__ppis_pattern = re.compile("\[Ppis.*\]", re.IGNORECASE)
	__fixed_pcd_pattern = re.compile("\[FixedPcd.*\]", re.IGNORECASE)
	__feature_pcd_pattern = re.compile("\[FeaturePcd.*\]", re.IGNORECASE)
	__generic_header_pattern = re.compile("\[.*\]", re.IGNORECASE)

	def __init__(self):

		"""Initializes some of the member variables of the object."""

		self.inf_version = ''
		self.base_name = ''
		self.file_guid = ''
		self.module_type = ''
		self.version_string = ''
		self.entry_point = ''

		self.defines = set()
		self.sources = set()
		self.packages = set()
		self.library_classes = set()
		self.protocols = set()
		self.guids = set()
		self.pcds = set()
		self.depexs = set()
		self.ppis = set()
		self.fixed_pcds = set()
		self.feature_pcds = set()

	def parse_inf_file(self, path_to_inf_file):

		"""Converts the .txt representation of an .inf file into an object representation."""

		"""Arguments:
			path_to_inf_file: Absolute path to the .inf to be converted.
		"""

		section = 0;

		with open(path_to_inf_file) as inf_file:
			
			for line in inf_file:

				#skip empty lines
				if line.isspace():
					continue;

				#Detect a new section of the file
				if self.__defines_pattern.search(line):
					section = sections.SECTION_DEFINES
					continue

				elif self.__source_pattern.search(line):
					section = sections.SECTION_SOURCES
					continue

				elif self.__package_pattern.search(line):
					section = sections.SECTION_PACKAGES
					continue

				elif self.__library_class_pattern.search(line):
					section = sections.SECTION_LIBRARYCLASSES
					continue

				elif self.__protocol_pattern.search(line):
					section = sections.SECTION_PROTOCOLS
					continue

				elif self.__guid_pattern.search(line):
					section = sections.SECTION_GUIDS
					continue

				elif self.__pcd_pattern.search(line):
					section = sections.SECTION_PCD
					continue

				elif self.__depex_pattern.search(line):
					section = sections.SECTION_DEPEX
					continue

				elif self.__buildop_pattern.search(line):
					section = sections.SECTION_BUILDOP
					continue

				elif self.__fixed_pcd_pattern.search(line):
					section = sections.SECTION_FIXEDPCD
					continue

				elif self.__feature_pcd_pattern.search(line):
					section = sections.SECTION_FEATUREPCD
					continue

				elif self.__ppis_pattern.search(line):
					section = sections.SECTION_PPIS
					continue

				elif self.__generic_header_pattern.search(line):
					section = sections.SECTION_GENERICHEADER
					continue

				elif re.search("^\s*(#+|/{2}).*$", line):  #Ignore comment lines
					continue

				#If no new section is detected then assign the value of the current line to the corresponding field of the infFileContents Object 
				
				#Defines section needs a special handling
				if section != sections.SECTION_DEFINES:
					line = line.split()[0]

				if section == sections.SECTION_DEFINES:
					
					var_name, data = line.split("=")
					var_name = var_name.strip()
					data = data.strip()

					if "INF_VERSION" in var_name:
						self.inf_version = data;
					elif "BASE_NAME" in var_name:
						self.base_name = data;
					elif "FILE_GUID" in var_name:
						self.file_guid = data;
					elif "MODULE_TYPE" in var_name:
						self.module_type = data;
					elif "VERSION_STRING" in var_name:
						self.version_string = data;
					elif "ENTRY_POINT" in var_name:
						self.entry_point = data;

				elif section == sections.SECTION_SOURCES:
					self.sources.add(line)

				elif section == sections.SECTION_PACKAGES:
					self.packages.add(line)

				elif section == sections.SECTION_LIBRARYCLASSES:
					self.library_classes.add(line)

				elif section == sections.SECTION_PROTOCOLS:
					self.protocols.add(line)

				elif section == sections.SECTION_GUIDS:
					self.guids.add(line)

				elif section == sections.SECTION_PCD:
					self.pcds.add(line.split('.')[1])

				elif section == sections.SECTION_DEPEX:
					self.depexs.add(line)

				elif section == sections.SECTION_PPIS:
					self.ppis.add(line)

				elif section == sections.SECTION_FIXEDPCD:
					self.fixed_pcds.add(line.split('.')[1])

				elif section == sections.SECTION_FEATUREPCD:
					self.feature_pcds.add(line.split('.')[1])

				elif section == sections.SECTION_GENERICHEADER:  #If it is a header that is not to be considered then skip that line.
					pass

		inf_file.close()

	def printInfObject(self):

		"""Prints the object representation of the .inf file."""

		print("\nDefines: \n")
		print("INF_VERSION: " + self.inf_version + "\n");
		print("BASE_NAME: " + self.base_name + "\n");
		print("FILE_GUID: " + self.file_guid + "\n");
		print("MODULE_TYPE: " + self.module_type + "\n");
		print("VERSION_STRING: " + self.version_string + "\n");
		print("ENTRY_POINT: " + self.entry_point + "\n");
		
		print("\nSources: \n")
		for element in self.sources:
			print(element)
		
		print("\nPackages: \n")
		for element in self.packages:
			print(element)
		
		print("\nLibraryClasses: \n")
		for element in self.library_classes:
			print(element)
		
		print("\nProtocols: \n")
		for element in self.protocols:
			print(element)
		
		print("\nGUIDs: \n")
		for element in self.guids:
			print(element)
		
		print("\nPCDs: \n")
		for element in self.pcds:
			print(element)
		
		print("\nDEPEX: \n")
		for element in self.depexs:
			print(element)

		print("\nPPIS: \n")
		for element in self.ppis:
			print(element)

		print("\nFixed PCDs: \n")
		for element in self.fixed_pcds:
			print(element)

		print("\nFeature PCDs: \n")
		for element in self.feature_pcds:
			print(element)