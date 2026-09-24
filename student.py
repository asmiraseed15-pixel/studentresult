class Student:
    """Represents a student."""

    def __init__(self, student_id, name, age, department):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department

    def display(self):
        print("\nStudent Details")
        print("-" * 30)
        print(f"ID         : {self.student_id}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Department : {self.department}")