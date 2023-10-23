import json


def process_class_schedule(input_file):
    with open(input_file, 'r') as file:
        classschedule_data = json.load(file)
    terms = set()
    for course in classschedule_data:
        for term in classschedule_data[course]:
            terms.add(term)
    return classschedule_data


if __name__ == "__main__":
    input_file = "/home/akshith/Desktop/SmartClassPlanningTool/Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json"
    process_class_schedule(input_file)
