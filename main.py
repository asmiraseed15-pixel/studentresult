"""
main.py
Command-line interface for the Student Result Management System.
Run this file to launch an interactive menu-driven program.
"""

from manager import StudentManager
from exceptions import (
    StudentNotFoundError,
    DuplicateStudentError,
    InvalidMarksError,
    EmptyDataError,
)

MENU_TEXT = """
=====================================
   STUDENT RESULT MANAGEMENT SYSTEM
=====================================
1. Add new student
2. View all students
3. Search student by ID
4. Search students by name
5. Update student name
6. Add / update subject marks
7. Delete a subject from a student
8. Delete a student
9. Class report (topper, average, pass/fail)
0. Exit
=====================================
"""


def prompt_marks():
    """Prompt the user to enter subject:marks pairs until they choose to stop."""
    marks = {}
    print("Enter subject and marks (leave subject blank to stop).")
    while True:
        subject = input("  Subject: ").strip()
        if not subject:
            break
        try:
            score = float(input(f"  Marks for {subject} (0-100): ").strip())
        except ValueError:
            print("  Please enter a valid number for marks. Skipping this subject.")
            continue
        marks[subject] = score
    return marks


def handle_add_student(manager):
    student_id = input("Enter new student ID: ").strip()
    name = input("Enter student name: ").strip()
    marks = prompt_marks()
    try:
        student = manager.add_student(student_id, name, marks)
        print(f"\nStudent added successfully:\n{student}")
    except DuplicateStudentError as exc:
        print(f"\nError: {exc}")
    except InvalidMarksError as exc:
        print(f"\nError: {exc}")


def handle_view_all(manager):
    students = manager.list_all_students()
    if not students:
        print("\nNo student records found.")
        return
    print(f"\nTotal students: {len(students)}")
    for student in students:
        print(student)


def handle_search_by_id(manager):
    student_id = input("Enter student ID to search: ").strip()
    try:
        student = manager.get_student(student_id)
        print(f"\n{student}")
    except StudentNotFoundError as exc:
        print(f"\nError: {exc}")


def handle_search_by_name(manager):
    keyword = input("Enter name (or part of name) to search: ").strip()
    matches = manager.search_by_name(keyword)
    if not matches:
        print("\nNo matching students found.")
        return
    for student in matches:
        print(student)


def handle_update_name(manager):
    student_id = input("Enter student ID: ").strip()
    new_name = input("Enter new name: ").strip()
    try:
        student = manager.update_student_name(student_id, new_name)
        print(f"\nUpdated:\n{student}")
    except StudentNotFoundError as exc:
        print(f"\nError: {exc}")


def handle_update_marks(manager):
    student_id = input("Enter student ID: ").strip()
    subject = input("Enter subject name: ").strip()
    try:
        score = float(input("Enter marks (0-100): ").strip())
    except ValueError:
        print("\nError: Marks must be a number.")
        return
    try:
        student = manager.update_subject_marks(student_id, subject, score)
        print(f"\nUpdated:\n{student}")
    except (StudentNotFoundError, InvalidMarksError) as exc:
        print(f"\nError: {exc}")


def handle_delete_subject(manager):
    student_id = input("Enter student ID: ").strip()
    subject = input("Enter subject to remove: ").strip()
    try:
        student = manager.delete_subject(student_id, subject)
        print(f"\nUpdated:\n{student}")
    except StudentNotFoundError as exc:
        print(f"\nError: {exc}")


def handle_delete_student(manager):
    student_id = input("Enter student ID to delete: ").strip()
    try:
        removed = manager.delete_student(student_id)
        print(f"\nDeleted student: {removed.name} (ID: {removed.student_id})")
    except StudentNotFoundError as exc:
        print(f"\nError: {exc}")


def handle_class_report(manager):
    try:
        if not manager.list_all_students():
            raise EmptyDataError("No students in the system yet.")
        topper = manager.class_topper()
        avg = manager.class_average()
        passing = manager.passing_students()
        failing = manager.failing_students()

        print(f"\nClass topper: {topper.name} (ID: {topper.student_id}, "
              f"Average: {topper.average_marks():.2f}, Grade: {topper.grade()})")
        print(f"Class average (of averages): {avg:.2f}")
        print(f"Students passing all subjects: {len(passing)}")
        print(f"Students failing at least one subject: {len(failing)}")
        if failing:
            print("  Failing students:")
            for student in failing:
                print(f"    - {student.name} (ID: {student.student_id})")
    except EmptyDataError as exc:
        print(f"\n{exc}")


def main():
    manager = StudentManager()
    actions = {
        "1": handle_add_student,
        "2": handle_view_all,
        "3": handle_search_by_id,
        "4": handle_search_by_name,
        "5": handle_update_name,
        "6": handle_update_marks,
        "7": handle_delete_subject,
        "8": handle_delete_student,
        "9": handle_class_report,
    }

    while True:
        print(MENU_TEXT)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("\nInvalid choice. Please try again.")
            continue

        try:
            action(manager)
        except Exception as exc:  # Final safety net so the program never crashes
            print(f"\nUnexpected error: {exc}")


if __name__ == "__main__":
    main()