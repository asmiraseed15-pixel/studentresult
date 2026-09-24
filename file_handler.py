"""
file_handler.py
Handles all reading/writing of student records to a CSV file.
Keeping file I/O separate from business logic (StudentManager) and
data modeling (Student) is a simple form of modular programming.
"""

import csv
import os

DEFAULT_FILE_PATH = "students.csv"
FIELDNAMES = ["student_id", "name", "marks"]


def load_students(file_path=DEFAULT_FILE_PATH):
    """
    Read student rows from the CSV file.

    Returns:
        list[dict]: A list of raw row dictionaries. Returns an empty list
        if the file does not exist yet (first run of the program).
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def save_students(students_dicts, file_path=DEFAULT_FILE_PATH):
    """
    Write a list of student dictionaries to the CSV file, overwriting
    any existing content.

    Args:
        students_dicts (list[dict]): Rows in the format produced by
            Student.to_dict().
        file_path (str): Destination CSV file path.
    """
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in students_dicts:
            writer.writerow(row)