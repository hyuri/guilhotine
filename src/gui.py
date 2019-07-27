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

import subprocess
import platform
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from tkinter.ttk import *

from constants import *

from folders import get_folder, set_folder
from memory import get_memory, set_memory, update_internal_memory, recall_last_folders
from shortcuts import bind_shortcuts
#from themes import get_theme_data

from books import output_chapters, output_metadata

#------------------------------------------------------------------------------

class StyleManager():
	def __init__(self, master):
		master.style = Style()

		master.style.configure("TLabelframe", padding=GUI_DEFAULT_MARGIN)
		master.style.configure("TLabelframe.Label", foreground="black", font="Helvetica 14 bold")
		master.style.configure("Path.TLabel", padding=(10, 10), font=PATH_FONT)
		master.style.configure("Title.TLabel", font=TITLE_FONT)
		master.style.configure("Subtitle.TLabel", font=SUBTITLE_FONT)
		master.style.configure("Big.TButton", font=GUI_BIG_BUTTON_FONT)

		# TODO: external theme loading system. Some initial heavy lifting work has already been done.
		# master.theme = get_theme_data("default")
		# master.current_theme = master.style.theme_use()
		# master.style.theme_create("MyStyle", parent=self.current_theme, settings=self.theme)

class TitleSubtitle(Frame):
	def __init__(self, master=None, title=APP_NAME, subtitle=None):
		super(TitleSubtitle, self).__init__()

		self.title_label = Label(master, text=title, style="Title.TLabel")
		self.title_label.pack()

		self.subtitle_label = Label(master, style="Subtitle.TLabel", text=subtitle)
		self.subtitle_label.pack()

class PathInput(Frame):
	def __init__(self, master, type_key, label=None, initial_path=None):
		super(PathInput, self).__init__()

		self.label_frame = LabelFrame(master, text=label)
		self.label_frame.pack(fill="x", expand=True, pady=GUI_DEFAULT_MARGIN)

		self.choose_button = Button(self.label_frame, text="Choose...", command=lambda: self.get_path(type_key))
		self.choose_button.pack(side="left")
		
		self.path_label = Label(self.label_frame, style="Path.TLabel", text=get_folder(type_key).resolve())
		self.path_label.pack(side="left")

	# Open folder browser
	def get_path(self, type_key):
		self.folder_path = filedialog.askdirectory(initialdir=get_memory("paths", f"last_{type_key}"))
		
		if not self.folder_path:
			return

		self.path_label["text"] = self.folder_path

		set_folder(type_key, Path(self.folder_path))
		set_memory("paths", f"last_{type_key}", Path(self.folder_path))

class MainPanel(Frame):
	def __init__(self, master=None, title="Untitled Window"):
		self.master = master
		self.title = self.master.title(title)

		super(MainPanel, self).__init__()

		self.style = StyleManager(self)

		#------------------------------------------------------------------------------
		# Title/Subtitle Labels
		self.title_subtitle = TitleSubtitle(self, subtitle="Bechapter Your Books")
		self.title_subtitle.pack()

		# Input Section
		self.input_path = PathInput(self, "input", "Input Folder")
		self.input_path.pack()

		# Output Section
		self.output_path = PathInput(self, "output", "Output Folder")
		self.output_path.pack()

		#------------------------------------------------------------------------------
		# Run Button
		self.run_button = Button(self, text="Run", command=self.output_files, style="Big.TButton")
		self.run_button.pack(fill="x", ipady=GUI_DEFAULT_MARGIN, pady=GUI_BIG_BUTTON_PADDING)

		#------------------------------------------------------------------------------
		# Shortcuts
		bind_shortcuts(self, "default")

	#------------------------------------------------------------------------------
	# Functions
	#------------------------------------------------------------------------------
	# Window management
	
	# Set minimum size. If run with no arguments, sets minsize to size at run
	def set_minsize(self, width=None, height=None):
		self.master.update()
		
		if not width:
			if not height:
				self.master.minsize(self.master.winfo_width(), self.master.winfo_height())
				return

			self.master.minsize(self.master.winfo_width(), height)
			return

		else:
			if height:
				self.master.minsize(width, height)
				return

			self.master.minsize(width, self.master.winfo_height())
			return

		self.master.minsize(width, height)

	# 
	def output_files(self):
		self.run_button["state"] = "disabled"

		text_files = [text_file for text_file in get_folder("input").glob("*.txt")]
		
		if not text_files:
			inform_failure(message="No text files found in this folder.\nPlease, choose another folder.", title="No Text Files Found")
			
			self.run_button["state"] = "normal"
			
			return
		
		output_chapters(text_files)
		output_metadata(text_files)

		inform_success()
		self.run_button["state"] = "normal"

		# Open file browser on output folder
		if platform.system() == "Darwin":
			subprocess.call(["open", str(get_folder("output").resolve())])

		elif platform.system() == "Windows":
			subprocess.call(["explorer", str(get_folder("output").resolve())])

		else:
			try:
				subprocess.call(["xdg-open", str(get_folder("output").resolve())])
			except:
				pass

	# Quit the entire application
	def quit(self):
		master.destroy()

#------------------------------------------------------------------------------
def run():
	window = Tk()

	main_panel = MainPanel(master=window, title=APP_NAME)
	main_panel.pack(fill=None, expand=True, padx=GUI_WINDOW_PADDING_X, pady=GUI_WINDOW_PADDING_Y)
	main_panel.set_minsize()

	main_panel.mainloop()

# Dialogs
def inform_success(title=APP_NAME, message="All Done!"):
	messagebox.showinfo(title, message)

def inform_failure(title=APP_NAME, message="Something went wrong. Double-check everything!"):
	messagebox.showerror(title, message)