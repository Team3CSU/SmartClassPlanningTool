import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog

from core.class_schedule import process_class_schedule
from core.prerequisite_graph import process_prerequisites
from core.recommendation import generate_degree_plan
from core.data_parser import extract_courses_from_pdf, extract_and_store_courses

app = tk.Tk()
app.title("SmartClassPlanning Tool")


def validate_files(file_paths):
    if "pdf" not in file_paths[0]:
        return False
    if "json" not in file_paths[1]:
        return False
    if "csv" not in file_paths[2]:
        return False
    return True


def browse_file(file_num):
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entries[file_num].delete(0, tk.END)
        file_entries[file_num].insert(0, file_path)


def submit_files():
    file_paths = [uploaded_file.get() for uploaded_file in file_entries]
    are_files_valid = validate_files(file_paths)

    if are_files_valid:
        text = extract_and_store_courses(file_paths[0])
        # texter = extract_courses_from_pdf(file_paths[0])
        graph = process_prerequisites(file_paths[1])
        schedule = process_class_schedule(file_paths[2])
        courses_to_take = generate_degree_plan(text, graph)
        print(courses_to_take)
    else:
        tkinter.messagebox.showwarning(title="yes", message="please provide required input files")


file_labels = ["Degree Works:", "Prerequisite Graph:", "Class Schedule:"]
file_entries = []

for i, label_text in enumerate(file_labels):
    label = tk.Label(app, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=10)

    entry = tk.Entry(app, width=50)
    entry.grid(row=i, column=1, padx=10, pady=10)
    file_entries.append(entry)

    browse_button = tk.Button(app, text="Browse", command=lambda i=i: browse_file(i))
    browse_button.grid(row=i, column=2, padx=10, pady=10)

submit_button = tk.Button(app, text="Submit", command=submit_files)
submit_button.grid(row=len(file_labels), column=1, padx=10, pady=20)

app.mainloop()
