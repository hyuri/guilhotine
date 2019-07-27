Specifications & Implementation Details

# Input
	- list of txt files. A folder, or a single file, are valid

# Output
	- 1 folder per text file
	- 1 .md file per chapter per text file
	- Naming should be: {0-n}.md

# Clean Up
	SPACES( ):
		- Merge neighboring duplicates
	
	HASHES(#):
		- Merge neighboring duplicates
		- All but the first one should have two preceding EOL chars and one following space char: ("\n\n# ")
	
	ASTERISKS(*):
		- Remove space after first and before second
		- Merge neighboring duplicates

# Format
	EOL CHARS(\n):
		- Double all EOL chars (replace "\n" with \n\n")

# Separate by Chapter
	- Chapters are separated by "# "
	- First 4 hash symbols belong to first chapter
	- The 3rd hash symbol is inline/not in a new line(doesn't have a preceding EOL char)
	- From 5th on, it's one hash symbol per chapter

# Generate Metadata(JSON)
	- "title": the Portuguese version—contained within first pair of parentheses in the file(which is immediatelly after the non-parenthesized English version)
	- "subtitle": contained within the second pair of parentheses in the file
	- "authors": not standardized. Usually what follows the string "Por " or "Do autor " but unreliable. Default: empty string | ""
	- "synopsis": not standardized. Default: empty string | ""
	- "targetAudience": starts at first ("\n" + 1 == "- ") after 3rd hash and ends at ("\n" + 1 != "- ")
	- "aboutAuthors": empty string ""
	- "coverUrl": empty string | ""
	- "categories": list containing two empty strings | ["", ""]
	- "translatedBy": empty string | ""
	- "narratedBy": empty string | ""
	- "mixedBy": empty string | ""
	- "uploadedBy": empty string | ""
	- purchased: empty string | ""
	- readingTime: the integer zero | 0
	- chapters: list containing a pair of curly brackets for each chapter in the file | [{}, {}, {}, ...]

#------------------------------------------------------------------------------
# High-Level Algorithm
1. Read Each Text Files
2. Clean Up and Format Each
3. Break Each Into Chapters
4. Write Each Chapter of each file Into one .md File, in Their Own Separate Folders