# Student Result Management System

A command-line Python application to manage student records and results.
Built to demonstrate core Python concepts: data structures, functions,
object-oriented programming, file handling, and exception handling.

## Features

- **Add students** with subject-wise marks
- **View all students**, sorted by ID
- **Search** by student ID or by name (partial match)
- **Update** a student's name or subject marks
- **Delete** a subject or an entire student record
- **Class report**: topper, class average, list of passing/failing students
- **Persistent storage** in a CSV file (`students.csv`) — data survives
  between runs
- **Automatic grade calculation** (A+ to F) based on average marks
- **Robust exception handling** with custom, meaningful exception types

## Project Structure

```
student_result_management/
├── main.py           # CLI entry point — menu-driven interface
├── manager.py         # StudentManager class — all CRUD & search logic
├── student.py         # Student class — the core data model (OOP)
├── file_handler.py    # CSV read/write functions (persistence layer)
├── exceptions.py       # Custom exception classes
├── students.csv        # Auto-created on first run — stores student data
└── README.md
```

This separation keeps each file focused on one responsibility
(modular programming):

- `student.py` — what a student *is*
- `file_handler.py` — how data is *saved/loaded*
- `manager.py` — the *business logic* that ties them together
- `main.py` — how the *user interacts* with the system

## Requirements

- Python 3.7 or higher (no external libraries needed — uses only the
  standard library: `csv`, `os`)

## How to Run

```bash
python3 main.py
```

You'll see a menu like this:

```
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
```

Enter the number of the action you want, and follow the prompts.

## Example Usage

```
Enter your choice: 1
Enter new student ID: 101
Enter student name: Asmina Parveen
Enter subject and marks (leave subject blank to stop).
  Subject: Math
  Marks for Math (0-100): 88
  Subject: Python
  Marks for Python (0-100): 95
  Subject:

Student added successfully:
ID: 101 | Name: Asmina Parveen | Math: 88, Python: 95 | Total: 183 | Average: 91.50 | Grade: A+
```

## Data Storage

Student records are stored in `students.csv` in the same folder as the
program. Each row stores the student ID, name, and a `subject:marks`
list (e.g. `Math:88;Python:95`). The file is created automatically the
first time you add a student, and is updated after every change — no
manual saving required.

## Error Handling

The system defines and handles custom exceptions instead of letting
the program crash:

| Exception               | Raised when...                                   |
|--------------------------|---------------------------------------------------|
| `StudentNotFoundError`   | Searching/updating/deleting an ID that doesn't exist |
| `DuplicateStudentError`  | Adding a student ID that already exists           |
| `InvalidMarksError`      | Marks entered are outside the 0–100 range         |
| `EmptyDataError`         | Generating a class report with no students        |

## Possible Extensions

- Export reports to PDF
- Add subject-wise class averages/toppers
- Add a simple GUI (Tkinter) or web interface (Flask)
- Switch storage to SQLite for larger datasets