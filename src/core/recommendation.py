from networkx import DiGraph


def has_prerequisites(course: str, graph: DiGraph):
    if graph.has_node(course):
        return True
    return False


def get_prerequisite(course: str, graph: DiGraph):
    for edge in graph.edges():
        if edge[0] == course:
            return edge[1]


def generate_degree_plan(text: dict, graph: DiGraph, Courseshedule:dict=None):
    courses_to_take = []

    # run a loop over all the keys of courses that have to be taken
    for key in text.keys():
        # extract courses for each key
        coursesRaw = text[key]
        counter = 0
        limit = 0
        courses = []
        for course in coursesRaw:
            course = course if "*" not in course else course[:course.find("*")]
            course = course.strip()
            course = " ".join(course.split());
            courses.append(course)
        
        for course in courses:
            if "SELECT".lower() in course.lower():
                # if there is a selection criteria, set it as a limit
                limit = int(course.split(" ")[1].strip())
            if limit > 0 and counter == limit:
                # if the selection criteria has been satisfied break the inner loop
                break
            if "SELECT".lower() not in course.lower():
                original_course = course
                # print(f"||{course}||is having pre requesite" if has_prerequisites(course, graph) else f"||{course}|| no preq")
                while has_prerequisites(course, graph):
                    course = get_prerequisite(course, graph)
                    if course is not None and course not in courses_to_take:
                        courses_to_take.append(course)
                if original_course not in courses_to_take: courses_to_take.append(original_course)
                counter = counter + 1
    return courses_to_take
