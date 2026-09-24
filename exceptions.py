"""
exceptions.py
Custom exception classes used across the Student Result Management System.
Using specific exceptions (instead of generic ones) makes error handling
clearer both for the developer and for anyone reading the code.
"""


class StudentNotFoundError(Exception):
    """Raised when a student ID is not found in the records."""
    pass


class DuplicateStudentError(Exception):
    """Raised when trying to add a student ID that already exists."""
    pass


class InvalidMarksError(Exception):
    """Raised when marks provided are outside the valid 0-100 range."""
    pass


class EmptyDataError(Exception):
    """Raised when an operation requires data but none is available."""
    pass