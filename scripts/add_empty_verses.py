#!/bin/python3

# append_bverse.py

import argparse
import os

def append_bverse(tex_file, num_verses):
    """
    Append specified number of \bverse{} lines to the given .tex file.
    
    Args:
        tex_file (str): Path to the .tex file
        num_verses (int): Number of \bverse{} lines to append
    """
    # Validate file
    if not os.path.exists(tex_file):
        raise FileNotFoundError(f"File '{tex_file}' does not exist.")
    if not tex_file.lower().endswith('.tex'):
        raise ValueError(f"File '{tex_file}' is not a .tex file.")
    
    # Validate number of verses
    if num_verses < 0:
        raise ValueError("Number of verses must be non-negative.")
    
    # Append \bverse{} lines
    with open(tex_file, "a", encoding="utf-8") as f:
        f.write("\n")
        for _ in range(num_verses):
            f.write("\\bverse{}\n")
    print(f"Appended {num_verses} \\bverse{{}} lines to '{tex_file}'.")


def process_input_file(input_file):
    """
    Read input file and append \bverse{} lines to corresponding .tex files.
    Args:
        input_file (str): Path to input file with book, chapter, verse counts
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # Split line into book-chapter and verse count (e.g., "Exodus 35:35 35")
                book_chapter, verse_count = line.split('\t')
                book, chapter = book_chapter.split()
                chapter_num = chapter.split(':')[0]
                verse_count = int(verse_count)
                
                # Construct .tex file path (e.g., ../books/exodus/exodus35.tex)
                book_filename = book.replace(" ", "_").replace("1_", "1").replace("2_", "2").replace("3_", "3").lower()
                tex_file = os.path.join("..", "books", book_filename, f"{book_filename}{chapter_num}.tex")
                
                # Append verses
                append_bverse(tex_file, verse_count)
            except ValueError as e:
                print(f"Skipping invalid line: '{line}' - {str(e)}")
            except Exception as e:
                print(f"Error processing line '{line}': {str(e)}")
                

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Append \\bverse{} lines to a .tex file.")
    parser.add_argument("-i", "--input", required=False, help="Path to the .tex file")
    parser.add_argument("-n", "--num_verses", type=int, required=False, help="Number of \\bverse{} lines to append")
    parser.add_argument("-f", "--file", required=True, help="Path to input file with book, chapter, verse counts")

    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        if args.file:
            process_input_file(args.file)
        elif args.input and args.num_verses is not None:
            append_bverse(args.input, args.num_verses)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
