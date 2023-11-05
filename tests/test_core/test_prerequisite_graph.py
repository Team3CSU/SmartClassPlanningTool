import json
import unittest
from unittest.mock import mock_open, patch

from src.core.prerequisite_graph import create_prerequisite_graph, process_prerequisites


class TestPrerequisiteGraph(unittest.TestCase):
    def test_create_prerequisite_graph(self):
        prerequisites_data = {
            "CourseA": ["Prerequisite1", "Prerequisite2"],
            "CourseB": ["Prerequisite3"],
        }

        graph = create_prerequisite_graph(prerequisites_data)

        # Check if the graph has the correct nodes and edges
        self.assertTrue(graph.has_node("CourseA"))
        self.assertTrue(graph.has_node("CourseB"))
        self.assertTrue(graph.has_edge("CourseA", "Prerequisite1"))
        self.assertTrue(graph.has_edge("CourseA", "Prerequisite2"))
        self.assertTrue(graph.has_edge("CourseB", "Prerequisite3"))

    @patch('builtins.open', new_callable=mock_open, create=True)
    def test_process_prerequisites(self, mock_file_open):
        input_file = "prerequisites.json"
        prerequisites_data = {
            "CourseA": ["Prerequisite1", "Prerequisite2"],
            "CourseB": ["Prerequisite3"],
        }

        # Mock the behavior of the open function to return JSON data
        mock_file_open.return_value.read.return_value = json.dumps(prerequisites_data)

        graph = process_prerequisites(input_file)

        # Check if the graph has the correct nodes and edges
        self.assertTrue(graph.has_node("CourseA"))
        self.assertTrue(graph.has_node("CourseB"))
        self.assertTrue(graph.has_edge("CourseA", "Prerequisite1"))
        self.assertTrue(graph.has_edge("CourseA", "Prerequisite2"))
        self.assertTrue(graph.has_edge("CourseB", "Prerequisite3"))


