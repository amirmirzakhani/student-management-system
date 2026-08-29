import os
import json
import matplotlib.pyplot as plt
from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON_PATH = os.path.join(BASE_DIR, "students.json")


class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        if isinstance(student, Student):
            self.students[student.id] = student
            self.save_to_json()
        else:
            raise ValueError("Only Student instances can be added.")

    def remove_student(self, student_id):
        student_id = str(student_id)
        if student_id in self.students:
            del self.students[student_id]
            self.save_to_json()
            return True
        return False

    def get_student(self, student_id):
        return self.students.get(str(student_id))

    def list_students(self):
        return self.students

    def update_student(self, student_id, **kwargs):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
            else:
                raise ValueError(f"Student has no attribute '{key}'")
        self.save_to_json()

    def display_all_students(self):
        if not self.students:
            print("No students found.")
            return
        for student in self.students.values():
            print(student)

    def get_top_student(self):
        if not self.students:
            return None
        return max(self.students.values(), key=lambda s: s.calculate_average())

    def sort_students_by_gpa(self):
        return sorted(
            self.students.values(),
            key=lambda s: s.calculate_average(),
            reverse=True
        )

    def calculate_overall_average(self):
        if not self.students:
            return 0.0
        total = sum(student.calculate_average() for student in self.students.values())
        return total / len(self.students)

    def save_to_json(self, filename=None):
        if filename is None:
            filename = DEFAULT_JSON_PATH

        data = [s.to_dict() for s in self.students.values()]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_json(self, filename=None):
        if filename is None:
            filename = DEFAULT_JSON_PATH

        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.students = {}
        for item in data:
            student = Student.from_dict(item)
            if student.id:
                self.students[student.id] = student
        print(f"Loaded {len(self.students)} students from {os.path.basename(filename)}")

    def generate_analytics_report(self):
        if not self.students:
            print("No data available for analytics.")
            return

        gpas = [s.calculate_average() for s in self.students.values()]
        avg_gpa = sum(gpas) / len(gpas)
        variance = sum((x - avg_gpa) ** 2 for x in gpas) / len(gpas)
        std_gpa = variance ** 0.5
        top_student = self.get_top_student()

        # محاسبه آمار رشته‌ها
        major_data = {}
        for s in self.students.values():
            major_data.setdefault(s.major, []).append(s.calculate_average())

        print("\n" + "=" * 55)
        print("📊 UNIVERSITY PERFORMANCE ANALYTICS")
        print("=" * 55)
        print(f"Total Enrolled Students : {len(self.students)}")
        print(f"University GPA Average  : {avg_gpa:.2f}")
        print(f"GPA Standard Deviation  : {std_gpa:.2f}")
        print(f"Top Performer           : {top_student.name} ({top_student.major}) - GPA: {top_student.calculate_average():.2f}")
        print("\n--- Major Performance Summary ---")
        print(f"{'Major':<25} | {'Count':<6} | {'Avg GPA':<8} | {'Max GPA':<8}")
        print("-" * 55)
        for major, scores in major_data.items():
            print(f"{major:<25} | {len(scores):<6} | {sum(scores)/len(scores):<8.2f} | {max(scores):<8.2f}")
        print("=" * 55 + "\n")

    def plot_analytics(self, save_fig=True):
        if not self.students:
            print("No data available to plot.")
            return

        gpas = [s.calculate_average() for s in self.students.values()]
        
        major_data = {}
        for s in self.students.values():
            major_data.setdefault(s.major, []).append(s.calculate_average())
        majors = list(major_data.keys())
        major_averages = [sum(scores)/len(scores) for scores in major_data.values()]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Student Performance Analytics", fontsize=14, fontweight="bold")

        axes[0].hist(gpas, bins=5, color="skyblue", edgecolor="black")
        axes[0].set_title("GPA Distribution")
        axes[0].set_xlabel("GPA")
        axes[0].set_ylabel("Count")
        axes[0].grid(axis="y", linestyle="--", alpha=0.7)

        axes[1].bar(majors, major_averages, color="salmon", edgecolor="black")
        axes[1].set_title("Average GPA by Major")
        axes[1].set_xlabel("Major")
        axes[1].set_ylabel("Average GPA")
        axes[1].set_ylim(0, 20)
        axes[1].tick_params(axis="x", rotation=45)
        axes[1].grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()

        if save_fig:
            output_path = os.path.join(BASE_DIR, "analytics_chart.png")
            plt.savefig(output_path, dpi=300)
            print(f"Analytics chart saved as '{output_path}'")

        plt.show()

    def plot_top_students(self, top_n=5, save_fig=True):
        if not self.students:
            print("No data available to plot.")
            return

        sorted_list = self.sort_students_by_gpa()[:top_n]
        names = [f"{s.name}\n({s.major})" for s in reversed(sorted_list)]
        gpas = [s.calculate_average() for s in reversed(sorted_list)]

        plt.figure(figsize=(9, 5))
        bars = plt.barh(names, gpas, color="#4C72B0", edgecolor="black", height=0.55)

        plt.title(f"Top {len(sorted_list)} Students by GPA", fontsize=13, fontweight="bold")
        plt.xlabel("GPA (out of 20)", fontsize=11)
        plt.xlim(0, 21)

        for bar in bars:
            width = bar.get_width()
            plt.text(
                width + 0.2,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.2f}",
                va="center",
                fontsize=10,
                fontweight="bold"
            )

        plt.grid(axis="x", linestyle="--", alpha=0.6)
        plt.tight_layout()

        if save_fig:
            output_path = os.path.join(BASE_DIR, "top_students_chart.png")
            plt.savefig(output_path, dpi=300)
            print(f"Top students chart saved as '{output_path}'")

        plt.show()