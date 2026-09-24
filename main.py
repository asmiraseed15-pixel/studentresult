import csv 
from student import Student
from result import Result


FILE_NAME = "students.csv"


def get_valid_mark(subject):
    """Get a valid mark between 0 and 100."""

    while True:
        try:
            mark = float(input(f"Enter {subject} mark: "))

            if 0 <= mark <= 100:
                return mark

            print("Mark must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def save_student(student, result):
    """Save student and result details into CSV file."""

    file_exists = False

    try:
        with open(FILE_NAME, "r", newline="") as file:
            file_exists = bool(file.read(1))
    except FileNotFoundError:
        file_exists = False

    with open(FILE_NAME, "a", newline="") as file:

        fieldnames = [
            "student_id",
            "name",
            "age",
            "department",
            "python",
            "maths",
            "english",
            "total",
            "average",
            "grade"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "department": student.department,
            "python": result.marks["Python"],
            "maths": result.marks["Maths"],
            "english": result.marks["English"],
            "total": result.total,
            "average": result.average,
            "grade": result.calculate_grade()
        })


def add_student():
    """Add a new student and save the result."""

    print("\n--- Add Student ---")

    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")

    while True:
        try:
            age = int(input("Enter age: "))

            if age > 0:
                break

            print("Age must be greater than 0.")

        except ValueError:
            print("Please enter a valid age.")

    department = input("Enter department: ")

    marks = {
        "Python": get_valid_mark("Python"),
        "Maths": get_valid_mark("Maths"),
        "English": get_valid_mark("English")
    }

    student = Student(
        student_id,
        name,
        age,
        department
    )

    result = Result(marks)

    save_student(student, result)

    print("\nStudent added successfully.")

    student.display()
    result.display_result()


def view_students():
    """Display all students stored in the CSV file."""

    print("\n--- Student Records ---")

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            records = list(reader)

            if not records:
                print("No student records found.")
                return

            for student in records:
                print("\n" + "-" * 40)
                print(f"ID         : {student['student_id']}")
                print(f"Name       : {student['name']}")
                print(f"Age        : {student['age']}")
                print(f"Department : {student['department']}")
                print(f"Total      : {student['total']}")
                print(f"Average    : {student['average']}")
                print(f"Grade      : {student['grade']}")

    except FileNotFoundError:
        print("No student records found.")


def search_student():
    """Search for a student using student ID."""

    search_id = input("Enter student ID to search: ")

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for student in reader:

                if student["student_id"] == search_id:
                    print("\nStudent Found")
                    print("-" * 30)
                    print(f"ID         : {student['student_id']}")
                    print(f"Name       : {student['name']}")
                    print(f"Age        : {student['age']}")
                    print(f"Department : {student['department']}")
                    print(f"Total      : {student['total']}")
                    print(f"Average    : {student['average']}")
                    print(f"Grade      : {student['grade']}")
                    return

            print("Student not found.")

    except FileNotFoundError:
        print("No student records found.")


def delete_student():
    """Delete a student using student ID."""

    student_id = input("Enter student ID to delete: ")

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            students = list(reader)

        updated_students = [
            student
            for student in students
            if student["student_id"] != student_id
        ]

        if len(students) == len(updated_students):
            print("Student not found.")
            return

        fieldnames = [
            "student_id",
            "name",
            "age",
            "department",
            "python",
            "maths",
            "english",
            "total",
            "average",
            "grade"
        ]

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(updated_students)

        print("Student deleted successfully.")

    except FileNotFoundError:
        print("No student records found.")


def main():
    """Run the Student Result Management System."""

    while True:

        print("\n================================")
        print(" STUDENT RESULT MANAGEMENT")
        print("================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()