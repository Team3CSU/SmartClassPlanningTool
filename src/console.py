

from core.class_schedule import process_class_schedule
from core.prerequisite_graph import process_prerequisites
from core.recommendation import generate_degree_plan
from core.data_parser import extract_courses_from_pdf, extract_and_store_courses
from core.excel_writer import create_excel_file



def validate_files(file_paths):
    if "pdf" not in file_paths[0]:
        return False
    if "json" not in file_paths[1]:
        return False
    if "json" not in file_paths[2]:
        return False
    return True


file_labels = ["Degree Works:", "Prerequisite Graph:", "Class Schedule:"]
file_entries = []

# for i, label_text in enumerate(file_labels):
#     label = tk.Label(app, text=label_text)
#     label.grid(row=i, column=0, padx=10, pady=10)

#     entry = tk.Entry(app, width=50)
#     entry.grid(row=i, column=1, padx=10, pady=10)
#     file_entries.append(entry)

#     browse_button = tk.Button(app, text="Browse", command=lambda i=i: browse_file(i))
#     browse_button.grid(row=i, column=2, padx=10, pady=10)

# submit_button = tk.Button(app, text="Submit", command=submit_files)
# submit_button.grid(row=len(file_labels), column=1, padx=10, pady=20)

# app.mainloop()

import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('f1', type=str, help='Path to the first file [Degree Works]',default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf")
    parser.add_argument('f2', type=str, help='Path to the second file [Prerequisite Graph]',default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq.json")
    parser.add_argument('f3', type=str, help='Path to the third file [Class Schedule]',default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json")
    parser.add_argument('file', type=str, help='Path to the results')
    args = parser.parse_args()

    # Now you can use args.file1, args.file2, and args.file3 to access the files
    file_paths = [args.f1, args.f2,  args.f3]
    are_files_valid = validate_files(file_paths)

    if are_files_valid:
        text = extract_and_store_courses(file_paths[0])
        print("\n\nExtracted courses:")
        for k in text: print(f"{k}  :                 {text[k]}")
        # texter = extract_courses_from_pdf(file_paths[0])
        print("\n\ngraph:")
        graph = process_prerequisites(file_paths[1])
        #schedule
        print("\n\schedule:")
        schedule = process_class_schedule(file_paths[2])
        courses_to_take = generate_degree_plan(text, graph,schedule)
        # print("\n\ncourses_to_ta
        create_excel_file(courses_to_take,args.file)
    else:
        print("Please provide valid input files.")


if __name__ == '__main__':
    main()
