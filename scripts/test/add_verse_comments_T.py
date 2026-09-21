#!/bin/python3
"""
Test add_verse_comments.py by processing the test fixture, writing the
result to an output file, and comparing the result against the expected
truth file.
"""

import os
import subprocess
import unittest


class AddVerseCommentsTest(unittest.TestCase):

    def test_add_verse_comments(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        test_file = os.path.join(
            script_dir,
            "test_files",
            "add_verse_comments_test_file.tex"
        )

        truth_file = os.path.join(
            script_dir,
            "test_files",
            "add_verse_comments_test_file_truth.tex"
        )

        output_file = os.path.join(
            script_dir,
            "test_files",
            "add_verse_comments_test_file_output.tex"
        )

        script_file = os.path.join(
            script_dir,
            "..",
            "add_verse_comments.py"
        )

        with open(test_file, "r", encoding="utf-8") as f:
            original = f.read()

        try:
            subprocess.run(
                ["python3", script_file, "-f", test_file, "--debug"],
                check=True
            )

            with open(test_file, "r", encoding="utf-8") as f:
                actual = f.read()

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(actual)

            with open(truth_file, "r", encoding="utf-8") as f:
                expected = f.read()

            self.assertEqual(expected, actual)

        finally:
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(original)


if __name__ == "__main__":
    unittest.main()
