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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Append \\bverse{} lines to a .tex file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the .tex file")
    parser.add_argument("-n", "--num_verses", type=int, required=True, help="Number of \\bverse{} lines to append")
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        append_bverse(args.input, args.num_verses)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
