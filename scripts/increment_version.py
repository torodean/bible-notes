#!/bin/python3

import re
import os

def increment_version(version_str):
    """
    Increment the minor part of a version string like 'Version 0.0057'.

    Args:
        version_str (str): The current version string.

    Returns:
        str: The incremented version string (e.g., 'Version 0.0058').
    """
    prefix, number = re.match(r'(Version\s+)(\d+\.\d+)', version_str).groups()
    major, minor = number.split('.')
    new_minor = f"{int(minor) + 1:04d}"
    return f"{prefix}{major}.{new_minor}"


def update_version(filename):
    """
    Update the version number in the given LaTeX file by incrementing it.

    Looks for a line like:
        \newcommand{\version}{Version 0.0057}

    Args:
        filename (str): Path to the LaTeX file to update.
    """
    with open(filename, 'r') as file:
        content = file.read()

    pattern = r'(\\newcommand{\\version}{)(Version\s+\d+\.\d+)(})'
    match = re.search(pattern, content)

    if match:
        old_version = match.group(2)
        new_version = increment_version(old_version)
        new_content = re.sub(pattern, rf'\1{new_version}\3', content)

        with open(filename, 'w') as file:
            file.write(new_content)
        print(f"Updated version: {old_version} → {new_version}")
    else:
        print("Version line not found.")


script_dir = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.abspath(os.path.join(script_dir, '..', 'bible-notes.tex'))
update_version(target_path)

