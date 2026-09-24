"""
student.py
Defines the Student class - the core data model for the
Student Result Management System.
"""


class Student:
    """Represents a single student and their subject-wise marks."""

    def __init__(self, student_id, name, marks=None):
        """
        Initialize a Student.

        Args:
            student_id (str): Unique identifier for the student (e.g. roll number).
            name (str): Full name of the student.
            marks (dict): Mapping of subject name -> marks obtained (0-100).
        """
        self.student_id = str(student_id)
        self.name = name
        self.marks = marks if marks is not None else {}

    def add_subject_marks(self, subject, score):
        """Add or update the marks for a single subject."""
        if not (0 <= score <= 100):
            raise ValueError(f"Marks for '{subject}' must be between 0 and 100.")
        self.marks[subject] = score

    def total_marks(self):
        """Return the sum of marks across all subjects."""
        return sum(self.marks.values())

    def average_marks(self):
        """Return the average marks, or 0 if no subjects are recorded."""
        if not self.marks:
            return 0.0
        return self.total_marks() / len(self.marks)

    def grade(self):
        """Compute a letter grade based on the average marks."""
        avg = self.average_marks()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        elif avg >= 35:
            return "E"
        else:
            return "F"

    def is_passing(self, pass_mark=35):
        """Return True if the student passes every subject individually."""
        return all(score >= pass_mark for score in self.marks.values())

    def to_dict(self):
        """Convert the student object into a flat dictionary for CSV storage."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "marks": ";".join(f"{subject}:{score}" for subject, score in self.marks.items()),
        }

    @classmethod
    def from_dict(cls, row):
        """Reconstruct a Student object from a CSV row (dictionary)."""
        marks = {}
        marks_field = row.get("marks", "")
        if marks_field:
            for pair in marks_field.split(";"):
                if not pair:
                    continue
                subject, score = pair.split(":")
                marks[subject] = float(score)
        return cls(row["student_id"], row["name"], marks)

    def __str__(self):
        marks_str = ", ".join(f"{sub}: {score}" for sub, score in self.marks.items()) or "No marks recorded"
        return (
            f"ID: {self.student_id} | Name: {self.name} | {marks_str} | "
            f"Total: {self.total_marks()} | Average: {self.average_marks():.2f} | "
            f"Grade: {self.grade()}"
        )