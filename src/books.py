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

import json

from constants import *
from folders import get_folder
from str_utils import replace_at,\
						replace_range,\
						remove_char,\
						insert_str,\
						get_encapsulated,\
						get_within_parentheses

#------------------------------------------------------------------------------
def get_chapters(text):
	"""Break into and return chapters.
	Expects formatted text."""

	hash_counter = 0
	previous_hash = -1

	# Find the end(index) of the first chapter
	for i in range(FIRST_CHAPTER_HASHES_COUNT + 1):
		previous_hash = text.find(CHAPTER_START, previous_hash + 1)
		hash_counter += 1

	chapters = []

	# Add first chapter to list of chapters
	first_chapter = text[:previous_hash].strip()
	chapters.append(first_chapter)

	# Add subsequent chapters
	second_hash = None

	remaining_len = len(text[previous_hash:])

	for i in range(remaining_len):
		second_hash = text.find(CHAPTER_START, previous_hash + 1)
		
		# If no more hashes found, add last chapter to the list and break out of the loop
		if second_hash == -1:
			last_chapter = text[previous_hash:].strip()
			chapters.append(last_chapter)
			break

		# Else, add next chapter to the list and update previous_hash
		next_chapter = text[previous_hash : second_hash].strip()
		chapters.append(next_chapter)

		previous_hash = second_hash

	return chapters

#------------------------------------------------------------------------------
# Formatting

# Return text formatted and cleaned up from all the issues
def get_formatted_text(text):
	# Remove double spaces, double asterisks and double hashes; Double EOLs; Fix inline(3rd) hash.
	# (i) Note that "fix_hashes" should always execute *before* "fix_eols",
	#     else one EOL will be missing before the inline(3rd) hash
	text = fix_invalid_chars(text)
	text = fix_hashes(text)
	text = fix_spaces(text)
	text = fix_asterisks(text)
	text = fix_eols(text)

	return text

# Fix space issues
def fix_spaces(text):
	# Remove double spaces and spaces before periods
	return text.replace("  ", " ").replace(" .", ".")

# Fix asterisk issues
def fix_asterisks(text):
	# Remove double asterisks
	text = text.replace("**", "*")

	asterisks_count = text.count("*")
	pairs_count = int(asterisks_count / 2) if (asterisks_count % 2) == 0 else int((asterisks_count - 1) / 2)

	# If we don't have at least one pair of asterisks, return text as is
	if pairs_count < 1:
		return text

	# Strip space between asterisks and the strings they encapsulate, and add space on their outside if not present
	for i in range(pairs_count):
		next_pair, opening_asterisk = get_encapsulated(text, "**", i + 1, tuple_with_index=True)
		closing_asterisk = text.find("*", opening_asterisk + 1)
		
		if not next_pair or closing_asterisk == -1:
			break

		try:
			if text[closing_asterisk + 1] not in [" ", ".", "("]:
				text = insert_str(text, " ", closing_asterisk + 1)
		except IndexError:
			pass
		
		text = replace_range(text, f"*{next_pair.strip()}*", opening_asterisk, closing_asterisk + 1)

		if text[opening_asterisk - 1] not in [" ", "\n"]:
			text = insert_str(text, " ", opening_asterisk)
	
	return text

# Fix inline(3rd) hash issue
def fix_inline_hash(text):
	return text.replace(" # ", "\n# ", 1)

# Sometimes the first hash is not followed by a space but it should
def fix_first_hash(text):
	return text.replace("#", CHAPTER_START, 1) if text[text.find("#") + 1] != " " else text

def fix_hashes(text):
	return fix_inline_hash(fix_first_hash(text.replace("##", "#")))

# Fix EOL issues
def fix_eols(text):
	# Assure two EOLs throughout. No more, no less
	eols_count = text.count("\n")
	previous_eol = -1

	for i in range(eols_count):
		next_eol = text.find("\n", previous_eol + 1)

		if text[next_eol - 1] != "\n":
			text = replace_at(text, "{}".format("\n" * EOLS_TARGET), next_eol)
			previous_eol = next_eol + (EOLS_TARGET - 1)

		else:
			text = remove_char(text, next_eol)
			previous_eol = next_eol - 1

	return text

def fix_invalid_chars(text):
	# Sometimes there are \u200b chars that break the encoding so we need to remove them
	return text.replace("\u200b", "")

# Metadata extraction

def get_chapters_count(text):
	"""Expects formatted text."""
	return text.count(CHAPTER_START) - (FIRST_CHAPTER_HASHES_COUNT - 1)

def get_title(text, subtitle=False):
	"""Expects formatted text."""
	title_start = text.find(CHAPTER_START) + len(CHAPTER_START)
	title_end = text.find("\n", title_start)
	
	title_line = text[title_start : title_end].strip()

	title = get_within_parentheses(title_line, 1)

	if subtitle:
		subtitle_start = text.find(CHAPTER_START, title_end + EOLS_TARGET) + len(CHAPTER_START)
		subtitle_end = text.find("\n", subtitle_start)
		
		# Setting title_line to "subtitle line"
		title_line = text[subtitle_start : subtitle_end]
		title = get_within_parentheses(title_line, 1)

	if not title:
		print("Title-Within-Parentheses not dectected. Using entire title line instead.")
		return title_line

	return title

def get_subtitle(text):
	"""Expects formatted text."""
	return get_title(text, subtitle=True)

def get_target_audience(text):
	"""Get from first "\n- " after preceding symbol(currently, 3rd hash) to "\n" + 1 != "-
	
	Expects formatted text.
	"""
	preceding_symbol_index = -1

	for i in range(TARGET_AUDIENCE_PRECEDING_SYMBOL_NUMBER):
		preceding_symbol_index = text.find(TARGET_AUDIENCE_PRECEDING_SYMBOL, preceding_symbol_index + 1)

	if preceding_symbol_index == -1:
		print("No third hash found.")

	start = text.find("{}- ".format("\n" * EOLS_TARGET), preceding_symbol_index + 1)
	end = start

	text_length = len(text)

	for i in range(text_length):
		next_eol = text.find("{}".format("\n" * EOLS_TARGET), end + EOLS_TARGET)
		
		if text[next_eol + EOLS_TARGET] == "-":
			end = next_eol
			continue
		
		end = next_eol
		break

	# Replace EOLs with one single EOL
	target_audience = text[start + EOLS_TARGET : end].replace("{}".format("\n" * EOLS_TARGET), "\n")

	# Remove semicolons and periods
	target_audience = target_audience.replace(";", "").replace(".", "")

	return target_audience

#------------------------------------------------------------------------------
# Outputting

def output_chapters(files):
	"""Expects formatted text."""

	for file in files:
		print(f"Outputting chapters for '{file.name}'")

		# Clean/Format and break text into its chapters
		chapters = get_chapters(get_formatted_text(file.read_text(encoding=TEXT_ENCODING)))

		# Create output folder if nonexistent
		try:
			(get_folder("output")/file.stem).mkdir()
		except FileExistsError:
			pass

		# Create subfolders if nonexistent
		for subfolder in ["text", "audio", "images"]:
			try:
				(get_folder("output")/file.stem/subfolder).mkdir()
			except FileExistsError:
				pass

		# Write chapters
		for i, chapter in enumerate(chapters):
			(get_folder("output")/file.stem/"text"/f"{i}.md").write_text(chapter, encoding=TEXT_ENCODING)

			print(i, end=" ")

		print("\n")
		print("Done.")

def output_metadata(files):
	for file in files:
		print(f"Outputting metadata(json) for '{file.name}'")

		# Clean/Format text
		formatted_text = get_formatted_text(file.read_text(encoding=TEXT_ENCODING))
		
		# Some properties are not currently detectable & have no functions to retrieve them. Default values follow specs
		title = get_title(formatted_text)
		subtitle = get_subtitle(formatted_text)
		authors = ""
		synopsis = ""
		target_audience = get_target_audience(formatted_text)
		about_authors = ""
		cover_url = ""
		categories_count = 2
		categories = ["" for i in range(categories_count)] # list of empty str times number of categories(default is 2 as per the specifications)
		translated_by = ""
		narrated_by = ""
		mixed_by = ""
		uploaded_by = ""
		purchase_url = ""
		reading_time = 0
		chapters_count = get_chapters_count(formatted_text)
		chapters = [{} for chapter in range(chapters_count)] # list of empty curly brackets times number of chapters

		# Check for properties that could not be retrieved, and inform the user
		not_retrieved = 0
		for i, element in enumerate([chapters_count, title, subtitle, authors, target_audience]):
			if element == None:
				not_retrieved += 1

		if not_retrieved > 0:
			print(f"(!) {i + 1} Properties could not be retrieved.\nCheck the output metadata file for missing values.")
		
		metadata = {
			"title": title,
			"subtitle": subtitle,
			"authors": authors,
			"synopsis": synopsis,
			"targetAudience": target_audience,
			"aboutAuthors": about_authors,
			"coverUrl": cover_url,
			"categories": categories,
			"translatedBy": translated_by,
			"narratedBy": narrated_by,
			"mixedBy": mixed_by,
			"uploadedBy": uploaded_by,
			"purchaseUrl": purchase_url,
			"readingTime": reading_time,
			"chapters": chapters
		}

		# Create output folder if nonexistent
		try:
			(get_folder("output")/file.stem).mkdir()
		except FileExistsError:
			pass
		
		try:
			(get_folder("output")/file.stem/"data.book.json").write_text(json.dumps(metadata, indent=JSON_INDENT_AMOUNT, ensure_ascii=IS_TEXT_ASCII))
		except UnicodeEncodeError:
			print(f"(!) Could not create metadata(.json) for '{file.name}'. Non-Unicode characters found in the input text.")

		print("Done.")