import sys
from student import Student
from manager import StudentManager


def print_menu():
    print("\n" + "=" * 45)
    print("🎓 STUDENT MANAGEMENT & ANALYTICS SYSTEM")
    print("=" * 45)
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. Search Student by ID")
    print("4. Update Student Information")
    print("5. Delete Student")
    print("6. Show Students Ranked by GPA")
    print("7. Generate Analytics Report")
    print("8. Plot Performance Analytics (Matplotlib)")
    print("9. Plot Top 5 Students Chart (Matplotlib)")
    print("0. Exit")
    print("=" * 45)


def main():
    manager = StudentManager()
    manager.load_from_json()

    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ").strip()

        if choice == "1":
            try:
                s_id = input("Enter Student ID: ").strip()
                if manager.get_student(s_id):
                    print("⚠️ Error: A student with this ID already exists.")
                    continue
                name = input("Enter Full Name: ").strip()
                major = input("Enter Major: ").strip()
                semester = int(input("Enter Semester: ").strip())
                email = input("Enter Email: ").strip()
                grades_input = input("Enter Grades (space-separated, e.g., 18.5 19 15): ").strip()
                grades = [float(g) for g in grades_input.split()] if grades_input else []

                new_student = Student(s_id, name, major, semester, email, grades)
                manager.add_student(new_student)
                print("✅ Student added and saved to JSON successfully.")
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

        elif choice == "2":
            print("\n--- ALL ENROLLED STUDENTS ---")
            manager.display_all_students()

        elif choice == "3":
            s_id = input("Enter Student ID to search: ").strip()
            student = manager.get_student(s_id)
            if student:
                print("\n" + str(student))
            else:
                print(f"⚠️ No student found with ID: {s_id}")

        elif choice == "4":
            s_id = input("Enter Student ID to update: ").strip()
            student = manager.get_student(s_id)
            if not student:
                print(f"⚠️ No student found with ID: {s_id}")
                continue

            print("Leave blank to keep current value.")
            new_name = input(f"New Name [{student.name}]: ").strip()
            new_major = input(f"New Major [{student.major}]: ").strip()
            new_sem = input(f"New Semester [{student.semester}]: ").strip()
            new_email = input(f"New Email [{student.email}]: ").strip()
            new_grades = input(f"New Grades (space-separated) [{student.grades}]: ").strip()

            updates = {}
            try:
                if new_name:
                    updates["name"] = new_name
                if new_major:
                    updates["major"] = new_major
                if new_sem:
                    updates["semester"] = int(new_sem)
                if new_email:
                    updates["email"] = new_email
                if new_grades:
                    updates["grades"] = [float(g) for g in new_grades.split()]

                if updates:
                    manager.update_student(s_id, **updates)
                    print("✅ Student updated and saved to JSON successfully.")
                else:
                    print("ℹ️ No changes made.")
            except ValueError as e:
                print(f"❌ Invalid update input: {e}")

        elif choice == "5":
            s_id = input("Enter Student ID to delete: ").strip()
            if manager.remove_student(s_id):
                print(f"🗑️ Student {s_id} deleted and saved to JSON.")
            else:
                print(f"⚠️ No student found with ID: {s_id}")

        elif choice == "6":
            sorted_students = manager.sort_students_by_gpa()
            if not sorted_students:
                print("No students enrolled.")
            else:
                print("\n--- STUDENTS RANKED BY GPA ---")
                for rank, s in enumerate(sorted_students, 1):
                    print(f"{rank}. {s.name} ({s.major}) - GPA: {s.calculate_average():.2f}")

        elif choice == "7":
            manager.generate_analytics_report()

        elif choice == "8":
            manager.plot_analytics(save_fig=True)

        elif choice == "9":
            manager.plot_top_students(top_n=5, save_fig=True)

        elif choice == "0":
            print("👋 Goodbye!")
            sys.exit(0)

        else:
            print("⚠️ Invalid choice. Please select from 0 to 9.")


if __name__ == "__main__":
    main()