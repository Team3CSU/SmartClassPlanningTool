import unittest
from unittest.mock import patch, mock_open
from src.core.class_schedule import process_class_schedule
import json

class TestClassSchedule(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_process_class_schedule(self, mock_file_open):
        # Mock the contents of the JSON file
        class_schedule_data = {'MATH 1113': ['Fa', 'Sp', 'Su'], 'MATH 2125': ['Fa', 'Sp', 'Su'], 'CPSC 1301K': ['Fa', 'Sp', 'Su'], 'CPSC 1302': ['Fa', 'Sp', 'Su'], 'CPSC 2105': ['Fa', 'Sp', 'Su'], 'MATH 5125': ['Fa', 'Sp', 'Su'], 'CPSC 2108': ['Fa', 'Sp', 'Su'], 'CYBR 2159': ['Fa', 'Sp'], 'CPSC 3175': ['Fa', 'Sp'], 'CYBR 2106': ['Fa', 'Sp', 'Su'], 'CPSC 3125': ['Fa', 'Sp'], 'CPSC 3131': ['Fa', 'Sp'], 'CPSC 3000+': ['Fa', 'Sp', '??'], 'CPSC 5135': ['Sp'], 'CPSC 3165': ['Fa', 'Sp', 'Su'], 'CPSC 3121': ['Sp'], 'CPSC 5115': ['Fa'], 'CPSC 4175': ['Fa'], 'CPSC 5157': ['Fa', 'Su'], 'CPSC 5155': ['Fa'], 'CPSC 5128': ['Sp'], 'CPSC 4176': ['Sp'], 'CPSC 4000': ['Fa', 'Sp', 'Su']}
        mock_file_open.side_effect = [
            mock_open(read_data=json.dumps(class_schedule_data)).return_value
        ]

        # Call the function with a mocked file
        input_file = "/path/to/your/fake/file.json"
        result = process_class_schedule(input_file)

        # Assertions
        self.assertEqual(result, class_schedule_data, "Expected class schedule data")
        mock_file_open.assert_called_once_with(input_file, 'r')

