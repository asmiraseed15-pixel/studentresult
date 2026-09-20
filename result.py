class Result:
    """Represents a student's academic result."""

    def __init__(self, marks):
        self.marks = marks
        self.total = sum(marks.values())
        self.average = self.total / len(marks)

    def calculate_grade(self):
        if self.average >= 90:
            return "A+"
        elif self.average >= 80:
            return "A"
        elif self.average >= 70:
            return "B"
        elif self.average >= 60:
            return "C"
        elif self.average >= 50:
            return "D"
        else:
            return "F"

    def display_result(self):
        print("\nResult")
        print("-" * 30)

        for subject, mark in self.marks.items():
            print(f"{subject:<15}: {mark}")

        print("-" * 30)
        print(f"Total          : {self.total}")
        print(f"Average        : {self.average:.2f}")
        print(f"Grade          : {self.calculate_grade()}")