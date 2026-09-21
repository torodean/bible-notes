#!/bin/python3
"""
Recursively replace \\bverse{} with \\bverse in all .tex files
under the specified directory.
"""

import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content.replace(r"\bverse{}", r"\bverse ")

    if updated != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)

        print(f"Updated: {file_path}")


def main():
    for root, _, files in os.walk(ROOT_DIR):
        for file_name in files:
            if file_name.endswith(".tex"):
                process_file(os.path.join(root, file_name))


if __name__ == "__main__":
    main()
