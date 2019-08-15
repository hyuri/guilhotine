#! python3
#-*- coding: utf-8 -*-

"""Guilhotine | Bechapter Your Books
Format/Clean Up and Break Book(text) Files Into Chapters. (See "specs.md" for details.)

| Credits:

Implementation:
	Hyuri Pimentel
"""

import os
from pathlib import Path

root = Path(os.path.dirname(os.path.realpath(__file__))).parent

folders = {
	"root": root,
	"src": root/"src",
	"io": root/"io",
	"input": root/"io"/"input",
	"output": root/"io"/"output",
	"settings": root/"settings",
	"shortcuts": root/"settings"/"shortcuts",
	"themes": root/"settings"/"themes",
	"memory": root/"settings"/"memory"
}

# Creating required default folders
for f in ["input", "output", "memory"]:
	try:
		folders[f].mkdir()

	except FileExistsError:
		pass

#------------------------------------------------------------------------------
# Functions

def get_folder(folder):
	return folders[folder]

def set_folder(folder, value):
	folders[folder] = value

	# TODO: save last path to memory
	# so we don't have to also call set_memory every time we set a folder
	# , memorize=True
	# if not memorize:
	# 	return

	# memory.set_memory("paths", f"last_{folder}", value)