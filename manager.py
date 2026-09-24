"""
manager.py
Defines StudentManager, the class responsible for all CRUD (Create, Read,
Update, Delete) and search operations on the collection of students.
This is the "business logic" layer that sits between the CLI (main.py)
and the data/storage layers (student.py, file_handler.py).
"""

from student import Student
from exceptions import StudentNotFoundError, DuplicateStudentError, InvalidMarksError
import file_handler


class StudentManager:
    """Manages an in-memory collection of Student objects with CSV persistence."""

    def __init__(self, file_path=file_handler.DEFAULT_FILE_PATH):
        self.file_path = file_path
        self.students = {}  # student_id -> Student
        self.load_from_file()

    # ---------- Persistence ----------

    def load_from_file(self):
        """Load students from the CSV file into memory."""
        rows = file_handler.load_students(self.file_path)
        self.students = {row["student_id"]: Student.from_dict(row) for row in rows}

    def save_to_file(self):
        """Persist the current in-memory students back to the CSV file."""
        rows = [student.to_dict() for student in self.students.values()]
        file_handler.save_students(rows, self.file_path)

    # ---------- Create ----------

    def add_student(self, student_id, name, marks=None):
        """
        Add a new student.

        Raises:
            DuplicateStudentError: if the student_id already exists.
            InvalidMarksError: if any provided mark is out of range.
        """
        student_id = str(student_id)
        if student_id in self.students:
            raise DuplicateStudentError(f"Student with ID '{student_id}' already exists.")

        new_student = Student(student_id, name)
        if marks:
            for subject, score in marks.items():
                try:
                    new_student.add_subject_marks(subject, score)
                except ValueError as exc:
                    raise InvalidMarksError(str(exc)) from exc

        self.students[student_id] = new_student
        self.save_to_file()
        return new_student

    # ---------- Read ----------

    def get_student(self, student_id):
        """
        Retrieve a single student by ID.

        Raises:
            StudentNotFoundError: if no student with that ID exists.
        """
        student_id = str(student_id)
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student found with ID '{student_id}'.")
        return self.students[student_id]

    def list_all_students(self):
        """Return all students, sorted by student_id."""
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def search_by_name(self, keyword):
        """Return all students whose name contains the given keyword (case-insensitive)."""
        keyword_lower = keyword.lower()
        return [s for s in self.students.values() if keyword_lower in s.name.lower()]

    # ---------- Update ----------

    def update_student_name(self, student_id, new_name):
        """Update a student's name."""
        student = self.get_student(student_id)
        student.name = new_name
        self.save_to_file()
        return student

    def update_subject_marks(self, student_id, subject, score):
        """
        Update (or add) marks for a subject for a given student.

        Raises:
            InvalidMarksError: if score is out of the valid 0-100 range.
        """
        student = self.get_student(student_id)
        try:
            student.add_subject_marks(subject, score)
        except ValueError as exc:
            raise InvalidMarksError(str(exc)) from exc
        self.save_to_file()
        return student

    # ---------- Delete ----------

    def delete_student(self, student_id):
        """
        Remove a student from the records.

        Raises:
            StudentNotFoundError: if no student with that ID exists.
        """
        student_id = str(student_id)
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student found with ID '{student_id}'.")
        removed = self.students.pop(student_id)
        self.save_to_file()
        return removed

    def delete_subject(self, student_id, subject):
        """Remove a single subject's marks from a student's record."""
        student = self.get_student(student_id)
        if subject in student.marks:
            del student.marks[subject]
            self.save_to_file()
        return student

    # ---------- Reporting ----------

    def class_topper(self):
        """Return the student with the highest average marks."""
        if not self.students:
            return None
        return max(self.students.values(), key=lambda s: s.average_marks())

    def class_average(self):
        """Return the average of averages across all students."""
        if not self.students:
            return 0.0
        return sum(s.average_marks() for s in self.students.values()) / len(self.students)

    def passing_students(self):
        """Return all students who pass every subject."""
        return [s for s in self.students.values() if s.is_passing()]

    def failing_students(self):
        """Return all students who fail at least one subject."""
        return [s for s in self.students.values() if not s.is_passing()]