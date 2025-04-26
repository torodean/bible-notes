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
    Process a single .tex file, replacing words and their plurals with word\index{Word}.
    Excludes text within \cite{} blocks.
    Places \index{} after words in \textit{} (e.g., \textit{hebrew}\index{Hebrew}) if not already present.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Step 1: Mask \cite{} blocks
        cite_placeholder = "__CITE_PLACEHOLDER_{}__"
        cite_blocks = []
        def store_cite(match):
            cite_blocks.append(match.group(0))
            return cite_placeholder.format(len(cite_blocks) - 1)

        content = re.sub(r'\\cite\{[^}]*\}', store_cite, content)

        modified = False
        # Step 2: Process non-italicized words
        for word in words:
            capitalized_word = word.capitalize()

            # Match word plus optional plural, excluding \index{} and \textit{}
            pattern = rf'(?<!\\index{{)(?<!\\textit{{)\b({re.escape(word)}(es|s)?)\b(?!\\index{{[^}}]*}})'
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

        # Step 3: Process italicized words
        for word in words:
            capitalized_word = word.capitalize()
            word_forms = [word, word + 's', word + 'es']
            for word_form in word_forms:
                index_pos = 0
                while True:
                    # Find word_form (case-insensitive)
                    content_lower = content.lower()
                    word_form_lower = word_form.lower()
                    word_start = content_lower.find(word_form_lower, index_pos)
                    if word_start == -1:
                        break
                    word_end = word_start + len(word_form)
                    actual_word = content[word_start:word_end]  # Preserve original case

                    # Check for \textit{ before
                    italic_start = word_start - 8
                    if italic_start >= 0 and content[italic_start:word_start] == '\\textit{':
                        # Check for closing }
                        if word_end < len(content) and content[word_end] == '}':
                            # Check for \index{ after
                            index_start = word_end + 1
                            if index_start + 7 >= len(content) or content[index_start:index_start + 7] != '\\index{':
                                # Add \index{}
                                index_word = capitalized_word if word_form == word else capitalized_word + word_form[-1]
                                replacement = f"\\textit{{{actual_word}}}\\index{{{index_word}}}"
                                original = f"\\textit{{{actual_word}}}"
                                content = content[:italic_start] + replacement + content[word_end + 1:]
                                GREEN = "\033[92m"
                                RESET = "\033[0m"
                                print(f"{GREEN}Replacing '{original}' with '{replacement}' in {file_path}{RESET}")
                                modified = True
                                index_pos = italic_start + len(replacement)
                            else:
                                index_pos = word_end + 1
                        else:
                            index_pos = word_end
                    else:
                        index_pos = word_end

        # Step 4: Restore \cite{} blocks
        for i, cite in enumerate(cite_blocks):
            content = content.replace(cite_placeholder.format(i), cite)

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
