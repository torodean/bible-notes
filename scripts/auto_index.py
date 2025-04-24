#!/bin/python3

import argparse
import os
import re

def read_words(file_path):
    """
    Read words from index_words.txt, one per line.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading index_words.txt: {e}")
        exit(1)

def process_tex_file(file_path, words):
    """
    Process a single .tex file, replacing words with \idx{word}.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False
        for word in words:
            # Capitalize the word for the index keyword (e.g., "heaven" -> "Heaven")
            capitalized_word = word.capitalize()
            # Regex to match word in the form word\index{...} (case-insensitive for word)
            # Capture the matched word to preserve its case
            pattern = rf'({re.escape(word)})\\index{{[^}}]*}}'
            # Replacement preserves the matched word's case (group 1) and uses capitalized word
            replacement = r'\1\\index{' + capitalized_word + '}'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes needed: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Replace words in .tex files with \\idx{word}")
    parser.add_argument('-i', '--index', type=str, help="Path to the index file to use.")
    parser.add_argument('-f', '--folder', type=str, help="Path to the folder containing .tex files")
    args = parser.parse_args()

    # Validate folder
    folder_path = args.folder
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        exit(1)

    # Read words from index_words.txt
    words_file = args.index
    if not os.path.isfile(words_file):
        print(f"Error: Index file not found!")
        exit(1)
    words = read_words(words_file)

    # Process all .tex files in the folder
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.tex'):
                file_path = os.path.join(root, file_name)
                process_tex_file(file_path, words)

if __name__ == "__main__":
    main()
