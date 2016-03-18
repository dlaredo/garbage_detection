import sys
import os
import os.path
import re
import stat
from garbageCollection import *

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

	gc = GarbageCorrection()
	gc.detect_unused_elements(root_directory, search_directory);


main();