import argparse
try:
    from core.class_schedule import process_class_schedule
    from core.prerequisite_graph import process_prerequisites
    from core.recommendation import generate_degree_plan
    from core.data_parser import extract_and_store_courses
    from core.excel_writer import create_excel_file
except:
    try:
        from src.core.class_schedule import process_class_schedule
        from src.core.prerequisite_graph import process_prerequisites
        from src.core.recommendation import generate_degree_plan
        from src.core.data_parser import extract_and_store_courses
        from src.core.excel_writer import create_excel_file
    except:
        print("Error: Could not import necessary modules")
        import sys
        sys.exit()
    

import os

# Get the path of the currently running Python script
script_path = os.path.realpath(__file__)

# Get the parent folder path
parent_folder = os.path.dirname(script_path)
parent_folder = os.path.dirname(parent_folder)

# Create the "logs" folder if it doesn't exist
logs_folder = os.path.join(parent_folder, "logs")

if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)
    print(f"Created 'logs' folder at {logs_folder}")
else:
    print(f"'logs' folder already exists at {logs_folder}")


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


def main():

    # Manually prompt for each file path instead of using argparse
    f1 = input('Enter the path to the first file [Degree Works] (default: "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf"): ')
    f2 = input('Enter the path to the second file [Prerequisite Graph] (default: "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq.json"): ')
    f3 = input('Enter the path to the third file [Class Schedule] (default: "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json"): ')
    output_file = input('Enter the path to the results file: ')

    # Provide default values if no input is given
    f1 = f1 or "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf"
    f2 = f2 or "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq.json"
    f3 = f3 or "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json"

    # Rest of your code remains the same
    file_paths = [f1, f2, f3]
    are_files_valid = validate_files(file_paths)

    if are_files_valid:
        text = extract_and_store_courses(file_paths[0],logsfolder=logs_folder)
        print("\n\nExtracted courses:")
        for k in text:
            print(f"{k}  :                 {text[k]}")
        print("\n\ngraph:")
        graph = process_prerequisites(file_paths[1])
        # schedule
        print("\n\nschedule:")
        schedule = process_class_schedule(file_paths[2])
        courses_to_take = generate_degree_plan(text, graph, schedule,logsfolder=logs_folder)
        create_excel_file(courses_to_take, output_file)
    else:
        print("Please provide valid input files.")


if __name__ == '__main__':
    main()
