class Student:
    def __init__(self, id, name, major, semester, email, grades=None):
        self.id = str(id)
        self.name = name
        self.major = major
        self.semester = int(semester)
        self.email = email
        self.grades = grades if grades is not None else []

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
            "grades": ";".join(map(str, self.grades))
        }

    @classmethod
    def from_dict(cls, data):
        grades_str = str(data.get("grades", ""))
        grades = (
            [float(g) for g in grades_str.split(";") if g.strip()]
            if grades_str and grades_str != "nan"
            else []
        )
        return cls(
            id=str(data["id"]),
            name=data["name"],
            major=data["major"],
            semester=int(data["semester"]),
            email=data["email"],
            grades=grades
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