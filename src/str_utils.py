#! python3
#-*- coding: utf-8 -*-

"""String Utils
A collection of useful tools for string manipulation.

By Hyuri Pimentel
"""

# Generic string utilities

def replace_at(dest_str, source_str, i):
	"""Replaces char at position "i" with string "source_src".
	If only one char is given, behaves exactly like the function "replace_char".
	"""
	return dest_str[:i] + str(source_str) + dest_str[i + 1:]

def replace_char(dest_str, char, i):
	"""Replaces char at position "i" with char "char"
	"""
	if len(str(char)) > 1:
		raise ValueError("too many characters. char must be one character long.")
	
	return dest_str[:i] + str(char) + dest_str[i + 1:]

def remove_char(dest_str, i):
	"""Removes char at position "i"
	"""

	return dest_str[:i] + dest_str[i + 1:]

def replace_range(dest_str, source_str, start, end):
	"""Replaces from "start" to "end" of a string "dest_str" with "source_str"
	"""
	return dest_str[:start] + str(source_str) + dest_str[end:]

def insert_str(dest_str, source_str, i):
	"""Inserts a string "source_str" into another string "dest_str" at position "i"
	"""
	return dest_str[:i] + source_str + dest_str[i:]

def overwrite_str(dest_str, source_str, i):
	"""Overwrites chars from position "i" to position "len(source_str)" with string "source_str"
	"""
	return dest_str[:i] + source_str + dest_str[i + len(source_str):]

#
def get_encapsulated(text, encapsulators, item_number, tuple_with_index=False):
	"""Expects formatted text.
	Needs clean up and optimization"""
	identical_encaps = [
		'""',
		"''",
	]

	if encapsulators[0] == encapsulators[1]:
		identical_encaps.append(encapsulators)

	# 
	iter_number = (item_number * 2) - 1 if encapsulators in identical_encaps else item_number
	
	encap_counter = 0
	opening_encap = -1

	for i in range(iter_number):
		next_encap = text.find(encapsulators[0], opening_encap + 1)
		
		if next_encap == -1:
			return

		opening_encap = next_encap
		encap_counter += 1

	closing_encap = text.find(encapsulators[1], opening_encap + 1)

	# Not found
	if closing_encap == -1:
		return

	if (closing_encap + 1) == len(text):
		encapsulated = text[opening_encap:].strip(encapsulators)

	else:
		encapsulated = text[opening_encap:closing_encap + 1].strip(encapsulators)

	if tuple_with_index:
		return (encapsulated, opening_encap)

	return encapsulated

def get_within_parentheses(text, item_number):
	"""Expects formatted text."""
	encapsulators = "()"

	prop = get_encapsulated(text, encapsulators, item_number)

	if not prop:
		return
	
	return prop