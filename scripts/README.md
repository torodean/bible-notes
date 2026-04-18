# Scripts

## Overview

This folder contains helper scripts which help with formatting, indexing, or other small tasks to simplify things that need done many times or over a large number of files. Descriptions of the scripts and what they do follow.

## append_bverse.py
Command-line utility for appending `\bverse{}` placeholders to LaTeX `.tex` files. Supports both single-file and batch processing modes. In batch mode, it reads an input file containing book, chapter, and verse counts, constructs corresponding `.tex` file paths, and appends the specified number of verse placeholders. Includes validation for file existence, file type, and input formatting, and skips invalid entries with error messages.

### How to use
```bash
# Batch mode
./add_empty_verses.py -f input.txt

# Single file mode
./add_empty_verses.py -i file.tex -n 10
```

## auto_index.py
Command-line utility for automatically inserting `\index{}` entries into LaTeX `.tex` files based on a predefined word list. Scans all `.tex` files in a target directory, matches words (including plural forms), and appends corresponding index entries while avoiding duplicates. Preserves LaTeX structure by excluding `\cite{}` blocks and correctly handling words inside `\textit{}` by appending index entries outside the italicized text. Includes validation for input files and directory paths, and outputs modifications during processing.

### How to use
```bash
./auto_index.py -i index_list.txt -f ../books
```

- i: Path to file containing words to index (default: index_list.txt)
- f: Directory containing .tex files to process (default: ../books)


## gen_books.py
Script for generating a structured set of LaTeX files for all books of the Bible. Creates a directory for each book, a main `.tex` file containing a `\booktitle{}` and commented `\input{}` references for each chapter, and individual chapter `.tex` files initialized with basic placeholders. Ensures existing files and directories are not overwritten, making it safe to run incrementally.

### How to use
```bash
./gen_books.py
```



## increment_version.py
Script for automatically incrementing the version number in a LaTeX file. Locates a `\newcommand{\version}{Version X.XXXX}` definition, increments the minor version (zero-padded to four digits), and updates the file in place. Targets a predefined LaTeX file relative to the script location and reports the version change.

### How to use
```bash
./increment_version.py
```


## lifespan_plotter.py
Script for visualizing lifespans as a horizontal bar chart using `matplotlib`. Defines a dataset of individuals with birth years and lifespans, sorts them chronologically, and plots each lifespan as a bar starting at the birth year. Includes visual alignment aids (dotted lines to the y-axis) and labeled axes for clarity.

### How to use
```bash
python lifespan_plotter.py
```


