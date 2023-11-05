from argparse import Namespace
import unittest
from unittest.mock import patch

from src import console
from src.console import validate_files


class TestConsole(unittest.TestCase):

    # test with valid inputs
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_valid_files(self, mock_parse_args):
        # Mock the command-line arguments
        f1 = "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input1.pdf"
        f2 = "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq2.json"
        f3 = "./Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json"
        file = "output.xlsx"
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

    # write code here to test with invalid files
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.console.validate_files', return_value=False)
    def test_main_with_invalid_files(self, mock_file_validator,mock_parse_args):
        # Mock the command-line arguments with invalid file paths
        f1 = "invalid_degree_works.txt"  # Example: Using a non-PDF file
        f2 = "invalid_prerequisite_graph.xml"  # Example: Using a non-JSON file
        f3 = "invalid_class_schedule.doc"  # Example: Using a non-JSON file
        file = "output.xlsx"
        mock_parse_args.return_value = Namespace(
            f1=f1,
            f2=f2,
            f3=f3,
            file=file
        )

        # with patch('src.console.validate_files') as mock_file_validator:
        with patch('src.console.extract_and_store_courses') as mock_extract:
            with patch('src.console.process_prerequisites') as mock_prerequisites:
                with patch('src.console.process_class_schedule') as mock_schedule:
                    with patch('src.console.generate_degree_plan') as mock_generate:
                        with patch('src.console.create_excel_file') as mock_create_excel:
                            console.main()
        
        self.assertFalse(mock_file_validator.return_value)
        
        # Assert that other mocked functions are not called
        mock_extract.assert_not_called()
        mock_prerequisites.assert_not_called()
        mock_schedule.assert_not_called()
        mock_generate.assert_not_called()
        mock_create_excel.assert_not_called()
        # Add assertions to check the expected behavior when input files are invalid
        # For example, assert that appropriate error messages are printed or exceptions raised.
        
    def test_valid_file_paths(self):
        # Test with valid file paths
        file_paths = ["sample.pdf", "data.json", "schedule.json"]
        result = validate_files(file_paths)
        self.assertTrue(result, "Expected True for valid file paths")

    def test_invalid_file_paths(self):
        # Test with invalid file paths
        # Case 1: Missing "pdf" in the first file
        file_paths = ["sample.txt", "data.json", "schedule.json"]
        result = validate_files(file_paths)
        self.assertFalse(result, "Expected False for missing 'pdf'")

        # Case 2: Missing "json" in the second file
        file_paths = ["sample.pdf", "data.txt", "schedule.json"]
        result = validate_files(file_paths)
        self.assertFalse(result, "Expected False for missing 'json'")

        # Case 3: Missing "json" in the third file
        file_paths = ["sample.pdf", "data.json", "schedule.txt"]
        result = validate_files(file_paths)
        self.assertFalse(result, "Expected False for missing 'json'")


