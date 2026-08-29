class Student:
    def __init__(self, id, name, major, semester, email, grades=None):
        self.id = str(id).strip()
        self.name = str(name).strip()
        self.major = str(major).strip()
        self.semester = int(semester)
        self.email = str(email).strip()
        self.grades = [float(g) for g in grades] if grades else []

    def calculate_average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "major": self.major,
            "semester": self.semester,
            "email": self.email,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            major=data.get("major", ""),
            semester=data.get("semester", 1),
            email=data.get("email", ""),
            grades=data.get("grades", [])
        )

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Major: {self.major}\n"
            f"Semester: {self.semester}\n"
            f"Email: {self.email}\n"
            f"Grades: {self.grades}\n"
            f"Average Grade: {self.calculate_average():.2f}\n"
            + "-" * 35
        )