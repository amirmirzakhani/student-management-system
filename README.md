f# 🎓 Student Management & Analytics System

A lightweight, object-oriented Student Management and Analytics System built with Python, JSON persistence, and Matplotlib visualizations.

---

## 📌 Features
- **Object-Oriented Architecture (OOP):** Modular design with `Student` and `StudentManager` classes.
- **Data Persistence:** Automatic and reliable state persistence using `JSON`.
- **Performance Analytics:** Comprehensive statistics including university GPA averages, standard deviations, and department summaries.
- **Visual Dashboards:** Built-in charts generated via `Matplotlib` (GPA distributions, average GPA by major, and top performers).
- **Interactive CLI:** Safe, robust command-line interface with comprehensive input handling.

---

## 🏗️ Project Structure
```text
├── student.py        # Student entity model & serialization
├── manager.py        # Business logic, analytics & visualization engine
├── main.py           # Interactive CLI user interface
├── students.json     # JSON database
├── .gitignore        # Ignored files configuration
└── README.md         # Project documentation