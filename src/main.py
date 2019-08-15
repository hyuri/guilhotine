#! python3
#-*- coding: utf-8 -*-

"""Guilhotine | Bechapter Your Books
Format/Clean Up and Break Book(text) Files Into Chapters. (See "specs.md" for details.)

| Credits:

Implementation:
	Hyuri Pimentel
"""

import argparse

from memory import update_internal_memory, recall_last_folders

import cli
import gui

#------------------------------------------------------------------------------

# Main
def main():
	update_internal_memory("paths")
	
	# If no command-line arguments provided, run in GUI mode
	if not cli.args.headless:
		recall_last_folders()
		gui.run()
		return
	
	# Else, run in headless mode
	cli.run()
	return

#------------------------------------------------------------------------------
if __name__ == "__main__":
	main()