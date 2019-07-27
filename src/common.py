#! python3
#-*- coding: utf-8 -*-

"""Guilhotine | Bechapter Your Books
Format/Clean Up and Break Book(text) Files Into Chapters. (See "specs.md" for details.)

| Credits:

Implementation:
	Hyuri Pimentel

Specifications:
	Guilherme Viotti
"""

from importlib.machinery import SourceFileLoader

from folders import folders

#------------------------------------------------------------------------------
# Functions

def get_resource(resource_name):
	populated_dict = dict()

	for file in folders[resource_name].glob(f"*.{resource_name[:-1] if resource_name.endswith('s') else resource_name}*"):
		populated_dict[file.stem] = file
	
	return populated_dict

def get_external_resource(path):
	return SourceFileLoader(f"__{path.stem}_loaded_resource__", str(path.resolve())).load_module()