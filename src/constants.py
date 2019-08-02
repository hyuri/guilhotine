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

APP_NAME = "Guilhotine"

#------------------------------------------------------------------------------
# Books
FIRST_CHAPTER_HASHES_COUNT = 4
EOLS_TARGET = 2
CHAPTER_START = "# "
TARGET_AUDIENCE_PRECEDING_SYMBOL = "#"
TARGET_AUDIENCE_PRECEDING_SYMBOL_NUMBER = 3

JSON_INDENT_AMOUNT = 2
TEXT_ENCODING = "utf-8"
IS_TEXT_ASCII = True if TEXT_ENCODING is "ascii" else False


#------------------------------------------------------------------------------
# GUI
#------------------------------------------------------------------------------
# Main Window
GUI_WINDOW_PADDING_X = 80
GUI_WINDOW_PADDING_Y = (GUI_WINDOW_PADDING_X/3, GUI_WINDOW_PADDING_X/1.5)

#------------------------------------------------------------------------------
# Fonts

DEFAULT_FONT_NAME = "Helvetica"
DEFAULT_FONT_SIZE = ""
DEFAULT_FONT_WEIGHT = "regular"
DEFAULT_FONT = f"{DEFAULT_FONT_NAME} {str(DEFAULT_FONT_SIZE)} {DEFAULT_FONT_WEIGHT}"

TITLE_FONT_SIZE = 24
TITLE_FONT_WEIGHT = "bold"
TITLE_FONT = f"{DEFAULT_FONT_NAME} {str(TITLE_FONT_SIZE)} {TITLE_FONT_WEIGHT}"

SUBTITLE_FONT_SIZE = 12
SUBTITLE_FONT_WEIGHT = "italic"
SUBTITLE_FONT = f"{DEFAULT_FONT_NAME} {str(SUBTITLE_FONT_SIZE)} {SUBTITLE_FONT_WEIGHT}"

PATH_FONT_SIZE = 14
PATH_FONT_WEIGHT = "italic"
PATH_FONT = f"{DEFAULT_FONT_NAME} {str(PATH_FONT_SIZE)} {PATH_FONT_WEIGHT}"

# Big Button
GUI_DEFAULT_MARGIN = 10
GUI_BIG_BUTTON_PADDING = 20

GUI_BIG_BUTTON_FONT_SIZE = 14
GUI_BIG_BUTTON_FONT_WEIGHT = "bold"
GUI_BIG_BUTTON_FONT = f"{DEFAULT_FONT_NAME} {str(GUI_BIG_BUTTON_FONT_SIZE)} {GUI_BIG_BUTTON_FONT_WEIGHT}"
