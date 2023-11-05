import argparse
from src.core.class_schedule import process_class_schedule
from src.core.prerequisite_graph import process_prerequisites
from src.core.recommendation import generate_degree_plan
from src.core.data_parser import extract_and_store_courses
from src.core.excel_writer import create_excel_file


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
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('f1', type=str, help='Path to the first file [Degree Works]',
                        default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf")
    parser.add_argument('f2', type=str, help='Path to the second file [Prerequisite Graph]',
                        default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq.json")
    parser.add_argument('f3', type=str, help='Path to the third file [Class Schedule]',
                        default="../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json")
    parser.add_argument('file', type=str, help='Path to the results')
    args = parser.parse_args()

    # print(args)
    # Now you can use args.file1, args.file2, and args.file3 to access the files
    file_paths = [args.f1, args.f2, args.f3]
    are_files_valid = validate_files(file_paths)

    if are_files_valid:
        text = extract_and_store_courses(file_paths[0])
        print("\n\nExtracted courses:")
        for k in text:
            print(f"{k}  :                 {text[k]}")
        print("\n\ngraph:")
        graph = process_prerequisites(file_paths[1])
        # schedule
        print("\n\nschedule:")
        schedule = process_class_schedule(file_paths[2])
        courses_to_take = generate_degree_plan(text, graph, schedule)
        create_excel_file(courses_to_take, args.file)
    else:
        print("Please provide valid input files.")


if __name__ == '__main__':
    main()
