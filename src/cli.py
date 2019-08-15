#! python3
#-*- coding: utf-8 -*-

"""Guilhotine | Bechapter Your Books
Format/Clean Up and Break Book(text) Files Into Chapters. (See "specs.md" for details.)

| Credits:

Implementation:
	Hyuri Pimentel
"""

import argparse
from pathlib import Path

from folders import get_folder
from books import output_chapters, output_metadata

#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="If run with no arguments, the GUI runs. Use -headless/--headless for headless version. Default input/output paths will be used, unless provided.")

parser.add_argument("--headless", "-headless", action="store_true", help=f"Run in headless mode/no GUI.")
parser.add_argument("-i", "--input", "-input", type=str, help=f"Output folder path.")
parser.add_argument("-o", "--output", "-output", type=str, help=f"Output folder path.")

args = parser.parse_args()

#------------------------------------------------------------------------------
def run():
	if args.input:
		set_folder("input", Path(args.input))
		set_memory("paths", "last_input", Path(args.input))
		print("Custom Input Folder: Set.")

	if args.output:
		set_folder("output", Path(args.output))
		set_memory("paths", "last_output", Path(args.output))
		print("Custom Output Folder: Set.")

	# Get list of files from the input folder
	text_files = [text_file for text_file in get_folder("input").glob("*.txt")]
	
	if not text_files:
		print("No text files found.")
		return
	
	output_chapters(text_files)
	output_metadata(text_files)

	# Inform success through a command-line prompt. Comment it out if you want auto exit after execution
	print("\nAll Done!")
	input("Press Enter to exit.")