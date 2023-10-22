#  parsing pdf
import re
from pdfminer.high_level import extract_text


def parse_course_requirements_from_pdf(input_file):
    try:
        text = extract_text(input_file)
        return parse_course_requirements(text)
    except Exception as e:
        print(f"Error reading PDF file: {str(e)}")
        return []


def parse_course_requirements(text):
    course_requirements = []
    current_category = None

    lines = text.split('\n')
    for line in lines:
        if line.strip():
            if re.match(r'^AREA [A-Z]+:', line):
                current_category = line.strip()
            elif current_category:
                match = re.match(r'\d+ Class(?:es)? in (.+)', line)
                if match:
                    course_requirements.append((current_category, match.group(1)))

    # TODO Extract further get list of courses to be done
    # print(course_requirements)
    return course_requirements


def extract_courses_from_pdf(pdf_file_path):
    course_data = {}  # Dictionary to store course data
    area = None  # Variable to track the current area

    text = extract_text(pdf_file_path)

    lines = text.split('\n')

    for line in lines:
        # Regular expressions to match course information
        area_match = re.search(r"AREA [A-Z]:\s+(.*)", line)
        course_match = re.findall(r"\b[A-Z]+\s+\d+[*@]?\b", line)

        if area_match:
            area = area_match.group(1)
        elif course_match:
            if area is not None:
                if area not in course_data:
                    course_data[area] = []
                course_data[area].extend(course_match)

    return course_data


def extract_and_store_courses(pdf_file_path):
    course_data = {}  # Dictionary to store course data
    current_area = None
    current_courses = []

    text = extract_text(pdf_file_path)
    for line in text.split('\n'):
        if re.search(r"AREA [A-Z]:", line):
            # Extract the area name
            current_area = re.search(r"AREA [A-Z]: (.+)", line).group(1).strip()
            current_courses = []
        #  CPSC 1223 CYBR MATH=> [A-Z]+\s+\d+[*] 
        elif re.search(r"Still Needed:.*?([A-Z]+\s+\d+[A-Z]?[*@]?)", line):
            # Extract course information (e.g., "1 Class in CPSC 1302*")
            match = re.findall(r"([A-Z]+\s+\d+[A-Z]?[*@]?)", line)
            current_courses.extend(match)
        elif current_area and not re.search(r"AREA [A-Z]:", line) and line.strip():
            # Continue to collect course information for the current area
            match = re.findall(r"([A-Z]+\s+\d+[A-Z]?[*@]?)", line)
            current_courses.extend(match)
        elif not current_area and line.strip():
            # Handle cases where the area is not explicitly mentioned
            match = re.findall(r"([A-Z]+\s+\d+[A-Z]?[*@]?)", line)
            current_courses.extend(match)

        if current_area:
            course_data[current_area] = current_courses

    return course_data


if __name__ == "__main__":
    # Example usage:
    pdf_file = "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf"  # Replace with your PDF file name
    requirements = parse_course_requirements_from_pdf(pdf_file)

    # Print the parsed course requirements
    for category, course in requirements:
        print(f"{category}\n{course}\n")
