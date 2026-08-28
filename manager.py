from student import Student


class StudentManager:

  def __init__(self):
    self.students = {}

  def add_student(self, student):
    if isinstance(student, Student):
      self.students[student.id] = student
    else:
      raise ValueError("Only Student instances can be added.")

  def remove_student(self, student_id):
    self.students.pop(student_id, None)

  def get_student(self, student_id):
    return self.students.get(student_id)

  def list_students(self):
    return self.students

  def update_student(self, student_id, **kwargs):
    student = self.get_student(student_id)
    if student:
      for key, value in kwargs.items():
        if hasattr(student, key):
          setattr(student, key, value)
        else:
          raise ValueError(f"Student has no attribute '{key}'")
    else:
      raise ValueError("Student not found.")

  def display_all_students(self):
    for student in self.students.values():
      print(student)
      print("-" * 40)  # Separator for better readability

  def get_top_student(self):
    if not self.students:
      return None
    return max(self.students.values(), key=lambda s: s.calculate_average())

  def sort_students_by_gpa(self):
    return sorted(
        self.students.values(),
        key=lambda s: s.calculate_average(),
        reverse=True,
    )

  def calculate_overall_average(self):
    if not self.students:
      return 0
    total = sum(
        student.calculate_average() for student in self.students.values()
    )
    return total / len(self.students)


