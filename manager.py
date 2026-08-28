import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        self.students.pop(str(student_id), None)

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

    def save_to_csv(self, filename="students.csv"):
        if not self.students:
            print("No students to save.")
            return
        data = [s.to_dict() for s in self.students.values()]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")

    def load_from_csv(self, filename="students.csv"):
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return
        df = pd.read_csv(filename)
        self.students = {}
        for _, row in df.iterrows():
            student = Student.from_dict(row.to_dict())
            self.students[student.id] = student
        print(f"Loaded {len(self.students)} students from {filename}")

    def generate_analytics_report(self):
        if not self.students:
            print("No data available for analytics.")
            return

        records = [
            {
                "ID": s.id,
                "Name": s.name,
                "Major": s.major,
                "Semester": s.semester,
                "GPA": s.calculate_average(),
                "Grades_Count": len(s.grades)
            }
            for s in self.students.values()
        ]

        df = pd.DataFrame(records)

        overall_mean = np.mean(df["GPA"])
        overall_std = np.std(df["GPA"])
        top_idx = df["GPA"].idxmax()
        top_student_row = df.loc[top_idx]

        print("\n" + "=" * 55)
        print("📊 UNIVERSITY PERFORMANCE ANALYTICS (NumPy & Pandas)")
        print("=" * 55)
        print(f"Total Enrolled Students : {len(df)}")
        print(f"University GPA Average  : {overall_mean:.2f}")
        print(f"GPA Standard Deviation  : {overall_std:.2f}")
        print(f"Top Performer           : {top_student_row['Name']} ({top_student_row['Major']}) - GPA: {top_student_row['GPA']:.2f}")
        print("\n--- GPA Summary by Major ---")
        major_stats = df.groupby("Major")["GPA"].agg(["count", "mean", "max"]).rename(
            columns={"count": "Students", "mean": "Avg GPA", "max": "Max GPA"}
        )
        print(major_stats)
        print("=" * 55 + "\n")

    def plot_analytics(self, save_fig=True):
        if not self.students:
            print("No data available to plot.")
            return

        records = [
            {"Major": s.major, "GPA": s.calculate_average()}
            for s in self.students.values()
        ]
        df = pd.DataFrame(records)

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Student Performance Analytics", fontsize=14, fontweight="bold")

        axes[0].hist(df["GPA"], bins=5, color="skyblue", edgecolor="black")
        axes[0].set_title("GPA Distribution")
        axes[0].set_xlabel("GPA")
        axes[0].set_ylabel("Count")
        axes[0].grid(axis="y", linestyle="--", alpha=0.7)

        major_avg = df.groupby("Major")["GPA"].mean()
        major_avg.plot(kind="bar", ax=axes[1], color="salmon", edgecolor="black")
        axes[1].set_title("Average GPA by Major")
        axes[1].set_xlabel("Major")
        axes[1].set_ylabel("Average GPA")
        axes[1].set_ylim(0, 20)
        axes[1].tick_params(axis="x", rotation=45)
        axes[1].grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()

        if save_fig:
            plt.savefig("analytics_chart.png", dpi=300)
            print("Analytics chart saved as 'analytics_chart.png'")

        plt.show()


if __name__ == "__main__":
    mgr = StudentManager()

    s1 = Student("101", "Sara", "Computer Science", 4, "sara@test.com", [18, 19.5, 15, 20])
    s2 = Student("102", "Ali", "Electrical Eng", 2, "ali@test.com", [12, 14, 11, 13.5])
    s3 = Student("103", "Reza", "Computer Science", 6, "reza@test.com", [19, 20, 18.5, 19])

    mgr.add_student(s1)
    mgr.add_student(s2)
    mgr.add_student(s3)

    mgr.save_to_csv()
    mgr.generate_analytics_report()
    mgr.plot_analytics(save_fig=True)