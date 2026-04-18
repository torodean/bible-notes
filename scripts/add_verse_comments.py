#!/bin/python3
"""
add_verse_comments.py

Recursively or selectively scans .tex files and inserts %verse comments above
each \bverse{} occurrence.

Rules:
- Only processes files with > MIN_VERSE_COUNT \bverse occurrences
- Adds sequential verse numbering starting at 1 per file
- Each FILE resets numbering
- If multiple \bverse occurrences appear on the SAME LINE, they are grouped:
    \bverse{}\bverse{}\bverse{}  -> %verse 1-3
- If \bverse occurs on separate lines, each line is numbered independently:
    \bverse{}                   -> %verse 1
    \bverse{}                   -> %verse 2
- Does NOT modify blank lines or add paragraph breaks

Supports:
- Single file mode
- Directory mode (recursive)
- Default: ../books
"""

import os
import re
import argparse


# -----------------------------
# CONFIG
# -----------------------------
VERSE_PATTERN = re.compile(r"\\bverse")
MIN_VERSE_COUNT = 4

DEBUG = False

def log(msg):
    if DEBUG:
        print(msg)

# -----------------------------
# INPUT HANDLING
# -----------------------------
def get_targets(single_file, folder):
    """
    Determine list of files to process based on CLI args.
    """
    if single_file:
        return [single_file]

    files = []
    for root, _, fns in os.walk(folder):
        for fn in fns:
            if fn.endswith(".tex"):
                files.append(os.path.join(root, fn))
    return files


# -----------------------------
# VALIDATION
# -----------------------------
def is_valid_file(file_path):
    """
    Only process files with enough \bverse occurrences.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return len(VERSE_PATTERN.findall(f.read())) > MIN_VERSE_COUNT
    except Exception:
        return False


# -----------------------------
# PARSING LOGIC
# -----------------------------
def analyze_lines(lines):
    """
    Identify verse structure.

    Returns:
        list of tuples:
        [
            (line_index, count_of_bverse_in_line)
        ]
    """
    result = []
    for i, line in enumerate(lines):
        count = len(re.findall(r"\\bverse", line))
        if count > 0:
            result.append((i, count))
    return result


# -----------------------------
# COMMENT FORMATTING
# -----------------------------
def format_comment(start, end):
    """
    Create %verse comment.
    """
    if start == end:
        return f"%verse {start}"
    return f"%verse {start}-{end}"


# -----------------------------
# CORE PROCESSING
# -----------------------------
def process_file(file_path):
    """
    Insert verse comments above relevant lines.
    Skips lines that already have a %verse comment immediately above them.
    """
    try:
        log(f"\n=== Processing file: {file_path} ===")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        verse_data = analyze_lines(lines)

        log(f"Found {len(verse_data)} lines containing \\bverse")

        if len(verse_data) <= MIN_VERSE_COUNT:
            log("Skipping (below threshold)")
            return

        verse_counter = 1
        offset = 0

        for line_idx, count in verse_data:
            adjusted_idx = line_idx + offset

            log(f"Line {line_idx} (adjusted {adjusted_idx}) has {count} \\bverse")

            # Skip if already processed
            if adjusted_idx > 0 and lines[adjusted_idx - 1].lstrip().startswith("%verse"):
                log(f"  -> Skipped (already has %verse)")
                verse_counter += count
                continue

            start = verse_counter
            end = verse_counter + count - 1

            comment = format_comment(start, end)

            log(f"  -> Inserting '{comment}' above line {adjusted_idx}")

            lines.insert(adjusted_idx, comment + "\n")

            offset += 1
            verse_counter += count

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        log(f"Finished: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# -----------------------------
# DRIVER
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Add %verse comments to LaTeX files.")

    parser.add_argument(
        "-f", "--file",
        help="Process a single .tex file"
    )

    parser.add_argument(
        "-d", "--dir",
        help="Directory to scan recursively (default: ../books)",
        default="../books"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )

    args = parser.parse_args()
    
    global DEBUG
    DEBUG = args.debug

    targets = get_targets(args.file, args.dir)

    for file_path in targets:
        if file_path.endswith(".tex") and is_valid_file(file_path):
            process_file(file_path)


if __name__ == "__main__":
    main()
