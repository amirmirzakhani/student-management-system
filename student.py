class Student:
    def __init__(self,id, name,major,semester, email, grades=None):
        self.id = id
        self.name = name
        self.major = major
        self.semester = semester
        self.email = email
        self.grades = grades if grades is not None else []

    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return f" ID: {self.id}\n Name: {self.name}\n Major: {self.major}\n Semester: {self.semester}\n Email: {self.email}\n Grades: {self.grades}\n Average Grade: {self.calculate_average()}"

    
student1 = Student(40313161077,"sara", "Computer Science", 5, "sara@example.com", [18,19.5,15,12,])
print(student1)
   