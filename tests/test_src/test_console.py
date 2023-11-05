from argparse import Namespace
import unittest
from unittest.mock import patch
from src import console  # Import the module you want to test

class TestConsole(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_valid_files(self, mock_parse_args):
        # Mock the command-line arguments
        f1="./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf"
        f2="./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq2.json"
        f3="./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json"
        file="output.xlsx"
        mock_parse_args.return_value = Namespace(
            f1=f1,
            f2=f2,
            f3=f3,
            file="output.xlsx"
        )
        with patch('src.console.extract_and_store_courses') as mock_extract:
            with patch('src.console.process_prerequisites') as mock_prerequisites:
                with patch('src.console.process_class_schedule') as mock_schedule:
                    with patch('src.console.generate_degree_plan') as mock_generate:
                        with patch('src.console.create_excel_file') as mock_create_excel:
                            console.main()
        mock_extract.assert_called_once_with(f1)
        mock_prerequisites.assert_called_once_with(f2)
        mock_schedule.assert_called_once_with(f3)
        mock_generate.assert_called_once()
        mock_create_excel.assert_called_once_with(mock_generate.return_value, "output.xlsx")

if __name__ == '__main__':
    unittest.main()
