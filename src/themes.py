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

themes = get_resource("themes")

#------------------------------------------------------------------------------
# Functions

def get_theme_data(theme_name):
	return get_external_resource(themes[theme_name]).theme_data