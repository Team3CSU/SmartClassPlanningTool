import unittest
from src.core.data_parser import (
    parse_course_requirements,
    extract_courses_from_pdf,
    extract_and_store_courses,
)


class TestDataParser(unittest.TestCase):
    def test_parse_course_requirements(self):
        # Test with sample text
        text = "AREA A:\n3 Classes in Math\nAREA B:\n2 Classes in Science\n"
        expected_requirements = [('AREA A:', 'Math'), ('AREA B:', 'Science')]
        result = parse_course_requirements(text)
        self.assertEqual(result, expected_requirements)

    def test_extract_courses_from_pdf(self):
        # Mock the text extracted from a PDF
        pdf_text = "AREA A: CourseA1 CourseA2\nAREA B: CourseB1 CourseB2 CourseB3\n"

        with unittest.mock.patch('pdfminer.high_level.extract_text', return_value=pdf_text):
            result = extract_courses_from_pdf("./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf")
        expected_course_data = {
            'SOCIAL SCIENCES': ['POLS 1101'], 'PROGRAM REQ': ['CPSC 3165', 'CPSC 4000'], 'TRACK REQ': ['CPSC 3121', 'CPSC 4115', 'CPSC 4135', 'CPSC 4148', 'CPSC 4155', 'CPSC 4157', 'CPSC 4175', 'CPSC 4176', 'CPSC 3', 'CYBR 3', 'MATH  3', 'DSCI  3111', 'STAT 3127']
        }

        self.assertEqual(result, expected_course_data)

    def test_extract_and_store_courses(self):
        # Mock the text extracted from a PDF
        pdf_text = "AREA A: CourseA1 CourseA2\nStill Needed: CourseA3 CourseA4\nAREA B: CourseB1 CourseB2\n"

        with unittest.mock.patch('pdfminer.high_level.extract_text', return_value=pdf_text):
            result = extract_and_store_courses("./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf")
        expected_course_data = {'SOCIAL SCIENCES': ['POLS 1101'], 'PROGRAM REQ': ['CPSC 3165*', 'CPSC 4000'], 'TRACK REQ': ['CPSC 3121*', 'CPSC 4115 ', 'CPSC 5115U*', 'CPSC 4135* ', 'CPSC 4148* ', 'CPSC 4155* ', 'CPSC 4157* ', 'CPSC 4175*', 'CPSC 4176*', 'DSCI  3111* ', 'STAT 3127*']}

        self.assertEqual(result, expected_course_data)


if __name__ == '__main__':
    unittest.main()
