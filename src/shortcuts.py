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

from common import *

shortcuts = get_resource("shortcuts")

#------------------------------------------------------------------------------
# Functions

def bind_shortcuts(master, name):
	get_external_resource(shortcuts[name]).bind(master)