#!/bin/python3

# generate_bible_books_single_data.py

import os

# Combined book data: (book_name, chapter_count)
books_data = [
    ("Genesis", 50), ("Exodus", 40), ("Leviticus", 27), ("Numbers", 36), ("Deuteronomy", 34),
    ("Joshua", 24), ("Judges", 21), ("Ruth", 4), ("1 Samuel", 31), ("2 Samuel", 24),
    ("1 Kings", 22), ("2 Kings", 25), ("1 Chronicles", 29), ("2 Chronicles", 36), ("Ezra", 10),
    ("Nehemiah", 13), ("Esther", 10), ("Job", 42), ("Psalms", 150), ("Proverbs", 31),
    ("Ecclesiastes", 12), ("Song of Solomon", 8), ("Isaiah", 66), ("Jeremiah", 52), ("Lamentations", 5),
    ("Ezekiel", 48), ("Daniel", 12), ("Hosea", 14), ("Joel", 3), ("Amos", 9),
    ("Obadiah", 1), ("Jonah", 4), ("Micah", 7), ("Nahum", 3), ("Habakkuk", 3),
    ("Zephaniah", 3), ("Haggai", 2), ("Zechariah", 14), ("Malachi", 4),
    ("Matthew", 28), ("Mark", 16), ("Luke", 24), ("John", 21), ("Acts", 28),
    ("Romans", 16), ("1 Corinthians", 16), ("2 Corinthians", 13), ("Galatians", 6), ("Ephesians", 6),
    ("Philippians", 4), ("Colossians", 4), ("1 Thessalonians", 5), ("2 Thessalonians", 3), ("1 Timothy", 6),
    ("2 Timothy", 4), ("Titus", 3), ("Philemon", 1), ("Hebrews", 13), ("James", 5),
    ("1 Peter", 5), ("2 Peter", 3), ("1 John", 5), ("2 John", 1), ("3 John", 1),
    ("Jude", 1), ("Revelation", 22)
]

# Base directory for all book folders
base_dir = "../books"

# Create base directory if it doesn't exist
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

for book, chapters in books_data:
    # Format book name for folder and filenames
    book_filename = book.replace(" ", "_").replace("1_", "1").replace("2_", "2").replace("3_", "3").lower()
    book_dir = os.path.join(base_dir, book_filename)
    
    # Create book directory only if it doesn't exist
    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    
    # Create main book file (e.g., genesis.tex) only if it doesn't exist
    main_filename = os.path.join(book_dir, f"{book_filename}.tex")
    if not os.path.exists(main_filename):
        with open(main_filename, "w", encoding="utf-8") as f:
            f.write(f"\\booktitle{{{book}}}{{}}\n")
            # Add \input commands for each chapter
            for chapter in range(1, chapters + 1):
                f.write(f"%\\input{{{os.path.join(base_dir, book_filename, f'{book_filename}{chapter}')}}}\n")
    
    # Create chapter files (e.g., genesis1.tex, genesis2.tex, etc.) only if they don't exist
    for chapter in range(1, chapters + 1):
        chapter_filename = os.path.join(book_dir, f"{book_filename}{chapter}.tex")
        if not os.path.exists(chapter_filename):
            with open(chapter_filename, "w", encoding="utf-8") as f:
                f.write(f"% Chapter {chapter} of {book}\n")
                f.write(f"\\bookchapter{{}}\n")
