import unittest
from networkx import DiGraph
from src.core.recommendation import PlaceCourse, cleanCourseCode, extractPreq, getEarliestAvailableSem, has_prerequisites, get_prerequisite,get_prerequisites, incAfter, newAcademicYr, sorter  # Replace 'your_module' with the actual module name

class TestPrerequisiteFunctions(unittest.TestCase):
    def setUp(self):
        # Create a sample directed graph (DiGraph) for testing
        self.graph = DiGraph()
        self.graph.add_node("CourseA")
        self.graph.add_node("CourseB")
        self.graph.add_node("CourseC")
        self.graph.add_node("CourseD")
        self.graph.add_node("CourseX")
        self.graph.add_node("CourseY")
        self.graph.add_edge("CourseA", "CourseB")
        self.graph.add_edge("CourseA", "CourseD")
        self.graph.add_edge("CourseB", "CourseC")
        self.graph.add_edge("CourseX", "CourseY")
        self.courses = {"CourseA", "CourseB", "CourseC", "CourseD"}
        self.AcadDict = {0: newAcademicYr()}

    def test_has_prerequisites_true(self):
        # Test if a course has prerequisites (should return True)
        result = has_prerequisites("CourseA", self.graph)
        self.assertTrue(result, "Expected True for a course with prerequisites")

    def test_has_prerequisites_false(self):
        # Test if a course has no prerequisites (should return False)
        result = has_prerequisites("CourseY", self.graph)
        self.assertFalse(result, "Expected False for a course with no prerequisites")

    def test_get_prerequisite_existing(self):
        # Test getting a prerequisite for a course with prerequisites
        result = get_prerequisite("CourseB", self.graph)
        self.assertEqual(result, "CourseC", "Expected 'CourseA' as a prerequisite")

    def test_get_prerequisite_non_existing(self):
        # Test getting a prerequisite for a course without prerequisites
        result = get_prerequisite("CourseY", self.graph)
        self.assertIsNone(result, "Expected None for a course without prerequisites")

    def test_get_prerequisites_existing(self):
        # Test getting prerequisites for a course with prerequisites
        result = get_prerequisites("CourseA", self.graph)
        expected_prerequisites = ["CourseB", "CourseD"]
        self.assertListEqual(result, expected_prerequisites, "Expected list of prerequisites")

    def test_get_prerequisites_non_existing(self):
        # Test getting prerequisites for a course without prerequisites
        result = get_prerequisites("CourseY", self.graph)
        self.assertListEqual(result, [], "Expected an empty list for a course without prerequisites")

    def test_cleanCourseCode_with_valid_courses(self):
        # Test with a list of courses that include valid courses
        # {"CourseA", "CourseB", "CourseC", "CourseD"}
        courses_raw = ["CourseA", "CourseB*", "Course E", "CourseD "]
        result = cleanCourseCode(courses_raw, self.courses)
        expected_result = ["CourseA", "CourseB", "CourseD"]
        self.assertListEqual(result, expected_result, "Expected a list of cleaned course codes")

    def test_cleanCourseCode_with_missing_courses(self):
        # Test with a list of courses that include missing courses
        courses_raw = ["CourseA", "CourseX*", "Course Y", "CourseZ"]
        result = cleanCourseCode(courses_raw, self.courses)
        expected_result = ["CourseA"]
        self.assertListEqual(result, expected_result, "Expected a list of cleaned course codes")

    def test_new_academic_year(self):
        # Call the function to create a new academic year dictionary
        result = newAcademicYr()

        # Check if the result is an empty semester dictionary
        expected_result = {"Fa": [], "Sp": [], "Su": []}
        self.assertEqual(result, expected_result, "Expected an empty semester dictionary")
    
    def test_sorter_with_empty_deps(self):
        # Test with an empty list of dependencies
        deps = []
        result = sorter(deps)
        self.assertEqual(result, -1, "Expected -1 for an empty list of dependencies")

    def test_sorter_with_non_empty_deps(self):
        # Test with a list of dependencies
        deps = [("CourseA", 2), ("CourseB", 1), ("CourseC", 3)]
        result = sorter(deps)
        self.assertEqual(result, 3, "Expected the maximum depth to be 3")
    
    def test_inc_after_with_valid_input(self):
        after = (0, 0)  # Start from the beginning of the academic year
        result = incAfter(after)
        self.assertEqual(result, (0, 1), "Expected next semester")

    def test_inc_after_overflow(self):
        after = (0, 2)  # Start from the end of the academic year
        result = incAfter(after)
        self.assertEqual(result, (1, 0), "Expected next year and first semester")

    def test_get_earliest_available_sem(self):
        course = "CourseA"
        CourseSchedule = {
            "CourseA": ["Fa", "Sp"],
            "CourseB": ["Sp", "Su"]
        }
        after = (0, 0)  # Start from the beginning of the academic year
        result = getEarliestAvailableSem(course, CourseSchedule, after)
        self.assertEqual(result, (0, 1), "Expected the next available semester")

    def test_get_earliest_available_sem_2(self):
        course = "CourseA"
        CourseSchedule = {
            "CourseA": [ "Fa"],
            "CourseB": ["Sp", "Su"]
        }
        after = (0, 0)  # Start from the beginning of the academic year
        result = getEarliestAvailableSem(course, CourseSchedule, after)
        self.assertEqual(result, (1, 0), "Expected the next available semester")

    def test_place_course_with_available_semester(self):
        course = "CourseA"
        CourseSchedule = {
            "CourseA": ["Fa", "Sp"],
            "CourseB": ["Sp", "Su"]
        }
        isdependency = False
        Sems = {0: {"Fa": ["CourseC"], "Sp": [], "Su": []}}
        after = (0, -1)  # Starting from the beginning of the academic year
        planned = PlaceCourse(course, CourseSchedule, isdependency, Sems, after)
        self.assertEqual(planned, (0, 0), "Expected the course to be planned in the next available semester")

    def test_place_course_with_available_semester_next_year(self):
        course = "CourseA"
        CourseSchedule = {
            "CourseA": ["Fa", "Sp"],
            "CourseB": ["Sp", "Su"]
        }
        isdependency = False
        Sems = {0: {"Fa": ["CourseC"], "Sp": [], "Su": []}}
        after = (0, 2)  # Starting from the beginning of the academic year
        planned = PlaceCourse(course, CourseSchedule, isdependency, Sems, after)
        self.assertEqual(planned, (1, 0), "Expected the course to be planned in the next available semester")

    def test_place_course_with_dependency(self):
        course = "CourseA"
        CourseSchedule = {
            "CourseA": ["Fa", "Sp"],
            "CourseB": ["Sp", "Su"]
        }
        isdependency = True
        Sems = {0: {"Fa": ["CourseC"], "Sp": [], "Su": []}}
        after = (0, -1)  # Starting from the beginning of the academic year
        planned = PlaceCourse(course, CourseSchedule, isdependency, Sems, after)
        self.assertEqual(planned, (0, 0), "Expected the course to be planned in the next available semester")

    def test_extractPreq(self):
        courses_to_take = []
        course = "CourseA" #,"CourseX"
        result =  extractPreq([],course,self.graph)
        self.assertTrue("CoursCA" not in result or "CourseB" not in result, "prerequestite Extraction Not functional")

