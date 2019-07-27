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

from pathlib import Path

import json

from folders import get_folder, set_folder

memory = {
	"paths": {
		"file": get_folder("memory")/"paths.memory",
		"last_input": get_folder("input"),
		"last_output": get_folder("output"),
		"last": get_folder("root")
	}
}

#------------------------------------------------------------------------------
# Functions

def get_memory_file(memory_key):
	return memory[memory_key]["file"]

def get_internal_memory(memory_key):
	fresh_memory = dict()

	# Populate dict with internal memory but all Path objects resolved and converted to strings. The file item is excluded
	for child_key in memory[memory_key]:
		if child_key != "file":
			fresh_memory[child_key] = str(memory[memory_key][child_key].resolve())

	return fresh_memory

def update_memory_file(memory_key):
	internal_memory = get_internal_memory(memory_key)
	
	get_memory_file(memory_key).write_text(json.dumps(internal_memory, indent=4))

def update_internal_memory(memory_key):
	memory_file = get_memory_file(memory_key)

	if not memory_file.exists():
		update_memory_file(memory_key)
		return

	memory_file_json = json.loads(memory_file.read_text())

	# Update internal memory dict with data from corresponding memory_file
	# All path strings are converted to Path objects.
	# The file item is excluded(It's supposed to never have been added anyways but it's another level of assurance)
	for child_key in memory[memory_key]:
		if child_key != "file":
			set_memory(memory_key, child_key, Path(memory_file_json[child_key]))

def get_memory(memory_key, child_key):
	update_internal_memory(memory_key)
	
	return memory[memory_key][child_key]

def set_memory(memory_key, child_key, value):
	# Update internal memory
	memory[memory_key][child_key] = value

	if memory_key == "paths":
		memory[memory_key]["last"] = value

	# Update memory file
	update_memory_file(memory_key)

# Change the input and output folders to the ones saved in memory
def recall_last_folders():
	set_folder("input", get_memory("paths", "last_input"))
	set_folder("output", get_memory("paths", "last_output"))