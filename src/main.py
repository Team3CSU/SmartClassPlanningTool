import tkinter as tk
from tkinter import filedialog
from core.data_parser import parse_course_requirements_from_pdf

app = tk.Tk()
app.title("SmartClassPlanning Tool")


def browse_file(file_num):
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entries[file_num].delete(0, tk.END)
        file_entries[file_num].insert(0, file_path)


def submit_files():
    # TODO handle input files
    file_paths = [uploaded_file.get() for uploaded_file in file_entries]
    print("Selected Files:")
    assert(file_entries[0].endswith(".pdf"))
    parse_course_requirements_from_pdf(file_entries[0])
    for file_path in file_paths:
        print(file_path)


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
