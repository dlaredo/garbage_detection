import os

class SourceFilesHandler(object):

	def look_for_elements_in_source_files(self, inf_file):

		"""Looks for elements such as Protocols, PPIS, GUIDs, etc in source files (.c or .h files)"""

		"""Parameters
			inf_file: Object representing the inf_file that contains the names of the source files where the function will look for elements
		"""

		"""Returns
			used_guids_set: Set containing the used GUIDs declared in this .inf file
			used_pcds_set: Set containing the used PCDs declared in this .inf file
			used_protocols_set: Set containing the used Protocols declared in this .inf file
			used_ppis_set: Set containing the used PPIS declared in this .inf file
			used_fixed_pcds_set: Set containing the used Fixed PCDs declared in this .inf file
			used_feature_pcds_set: Set containing the used Feature PCDs declared in this .inf file
			unexesting_files: List containing the names of the unexisting files declared in the .inf file
			unexesting_files_inf:
		"""
			
		used_guids_set, used_pcds_set, used_protocols_set, used_ppis_set, used_fixed_pcds_set, used_feature_pcds_set =\
		set(), set(), set(), set(), set(), set()
		unexesting_files = list()
		unexesting_files_inf = list()


		#Look for elements in source files
		for source_file_name in inf_file.sources:

			(source_name, source_ext) = os.path.splitext(source_file_name)

			#For each C file of the module (*.inf file)
			if source_ext == '.c' or source_ext == '.h':

				file_path = os.path.join(inf_file.path, source_file_name.replace("$(OPENSSL_PATH)", "openssl-0.9.8zf"))

				print("Analizing " + file_path)
				file_buffer = ''

				#Attempt to open the source file.
				try:
					#Load entire file into buffer
					with open(file_path, 'r', -1, 'utf-8') as source_file:
						file_buffer = source_file.read().replace('\n', ' ')
					source_file.close()
				except FileNotFoundError:
					unexesting_files.append(source_file_name)
					unexesting_files_inf.append(os.path.join(inf_file.path, inf_file.file_name))
				except Exception as e:
					#If the file can not be opened due to coding problems, attempt to open it in a different coding
					with open(file_path, 'r', -1, 'cp1252') as source_file:
						file_buffer = source_file.read().replace('\n', ' ')
					source_file.close()

				#find guids in file
				for guid in inf_file.guids:
					if file_buffer.find(guid) != -1:
						used_guids_set.add(guid)

				#find pcds in file
				for pcd in inf_file.pcds:
					if file_buffer.find(pcd) != -1:
						used_pcds_set.add(pcd)

				#find protocols in file
				for protocol in inf_file.protocols:
					if file_buffer.find(protocol) != -1:
						used_protocols_set.add(protocol)

				#find ppis in file
				for ppi in inf_file.ppis:
					if file_buffer.find(ppi) != -1:
						used_ppis_set.add(ppi)

				#find fixedpcd in file
				for fixed_pcd in inf_file.fixed_pcds:
					if file_buffer.find(fixed_pcd) != -1:
						used_fixed_pcds_set.add(fixed_pcd)

				#find featurepcd in file
				for feature_pcd in inf_file.feature_pcds:
					if file_buffer.find(feature_pcd) != -1:
						used_feature_pcds_set.add(feature_pcd)

		return used_guids_set, used_pcds_set, used_protocols_set, used_ppis_set, used_fixed_pcds_set, used_feature_pcds_set,\
		unexesting_files, unexesting_files_inf