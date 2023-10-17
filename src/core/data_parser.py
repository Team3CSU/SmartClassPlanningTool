#  parsing pdf
import re
from pdfminer.high_level import extract_text

def parse_course_requirements_from_pdf(pdf_file):
    try:
        text = extract_text(pdf_file)
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

    return course_requirements

if __name__=="__main__":
    # Example usage:
    pdf_file = "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf"  # Replace with your PDF file name
    requirements = parse_course_requirements_from_pdf(pdf_file)

    # Print the parsed course requirements
    for category, course in requirements:
        print(f"{category}\n{course}\n")
