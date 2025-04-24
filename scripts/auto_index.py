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

import re

def process_tex_file(file_path, words):
    """
    Process a single .tex file, replacing words and their plurals with word\index{Word}.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False
        for word in words:
            capitalized_word = word.capitalize()

            # Match base word plus optional plural suffix (naive pluralization)
            pattern = rf'(?<!\\index{{)\b({re.escape(word)}(es|s)?)\b(?!\\index{{[^}}]*}})'

            def repl(match):
                original_text = match.group(1)
                replacement_text = f"{original_text}\\index{{{capitalized_word}}}"
                GREEN = "\033[92m"
                RESET = "\033[0m"
                print(f"{GREEN}Replacing '{original_text}' with '{replacement_text}' in {file_path}{RESET}")
                return replacement_text

            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, repl, content, flags=re.IGNORECASE)
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Replace words in .tex files with word\\index{Word}")
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
