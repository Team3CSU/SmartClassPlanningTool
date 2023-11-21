from networkx import DiGraph
import os


def has_prerequisites(course: str, graph: DiGraph):
    # if graph.has_node(course):
    for edge in graph.edges():
        if edge[0] == course:
            return True
    return False


def get_prerequisite(course: str, graph: DiGraph):
    for edge in graph.edges():
        if edge[0] == course:
            return edge[1]


def get_prerequisites(course: str, graph: DiGraph):
    courses = []
    for edge in graph.edges():
        if edge[0] == course:
            courses.append(edge[1])
    return courses


def cleanCourseCode(coursesRaw: list, Courseshedule):
    courses = []
    for course in coursesRaw:
        if "SELECT" in course:
            courses.append(course)
            continue
        course = course if "*" not in course else course[:course.find("*")]
        course = course.strip()
        course = " ".join(course.split());
        if course in Courseshedule:
            courses.append(course)
        else:
            print('{} is missing'.format(course))
    return courses


def newAcademicYr():
    semester_dict = {"Fa": list().copy(), "Sp": list().copy(), "Su": list().copy()}
    return semester_dict


def sorter(deps):
    if (not deps):
        return -1
    depth = 0
    for code, crsdepth in deps:
        depth = max(depth, crsdepth)
    return depth


def extractPreq(courses_to_take, course, graph, lvl=0):
    dependencies = []
    if has_prerequisites(course, graph):
        preqCourses = get_prerequisites(course, graph)
        for preq in preqCourses:
            if preq is not None:
                if preq not in courses_to_take:
                    courses_to_take.append(preq)
                dependencies.append((preq, lvl))
                if has_prerequisites(preq, graph):
                    dep_in_depth, crsestake_indpth = extractPreq(courses_to_take, preq, graph, lvl + 1)
                    dependencies.extend(dep_in_depth)
                    courses_to_take = crsestake_indpth
    return dependencies, courses_to_take


def generate_degree_plan(text: dict, graph: DiGraph, Courseshedule: dict = None,logsfolder=None):
    courses_to_take = []
    logfile  = open(f'{logsfolder}/extracted_logs.txt', 'a')
    courses_plan_dict = {}
    coursecount = 0
    # run a loop over all the keys of courses that have to be taken
    for key in text.keys():
        # extract courses for each key
        coursesRaw = text[key]
        counter = 0
        limit = 0
        courses = cleanCourseCode(coursesRaw, Courseshedule)
        if logsfolder:
            print("\narea : "+ key,file = logfile)
            print("\n\t\traw =>",coursesRaw,file = logfile)
            print("\t\tclean=>",courses,file = logfile)
        print("*******"*20)
        
        for course in courses:
            dependencies = []
            if "SELECT".lower() in course.lower():
                # if there is a selection criteria, set it as a limit
                limit = int(course.split(" ")[1].strip())
            if limit > 0 and counter == limit:
                # if the selection criteria has been satisfied break the inner loop
                break
            if "SELECT".lower() not in course.lower():
                coursecount += 1
                original_course = course
                dependencies, courses_to_take = extractPreq(courses_to_take, original_course, graph)
                courses_plan_dict[original_course] = dependencies
                if original_course not in courses_to_take:
                    courses_to_take.append(original_course)
                counter = counter + 1
        if logsfolder:
            print("\n","courses_to_take",file = logfile)
            print(courses_to_take,file = logfile)
    # return courses_to_take,courses_plan_dict
    Sems = {0: newAcademicYr(), 1: newAcademicYr()}

    if logsfolder:
        print("\n\nExtracting prereq",file = logfile)
        for course in sorted(courses_plan_dict, key=lambda x: sorter(courses_plan_dict[x]), reverse=True):
            print("\t\tMain course: ",course,file = logfile)
            for dep in courses_plan_dict[course]:
                print("\t\t","\t"*(dep[1]+1),dep,file = logfile)
        print("Started planning",file = logfile)
    coursesTaken, planned = AcadPlanner(courses_plan_dict, Courseshedule, graph, Sems, courses_to_take, after=(0, -1),logfile=logfile)
    coursesTaken_last = AcadPlannerLast(courses_plan_dict, Courseshedule, Sems, courses_to_take,coursesTaken=coursesTaken,logfile=logfile)
    coursesTaken_c = [c for c, t in coursesTaken]

    return Sems


def AcadPlanner(courses_plan_dict, Courseshedule, graph, Sems, courses_to_take=None, coursesTaken=None, plandep=0,
                after=(0, -1),logfile=None):
    if not coursesTaken:
        coursesTaken = list()
    planed = None
    for course in sorted(courses_plan_dict, key=lambda x: sorter(courses_plan_dict[x]), reverse=True):
        if logfile:
            print("\t"*plandep,"planning course :",course,file = logfile)
        plannedmax = after
        planlst = [after]
        dependencies = courses_plan_dict.get(course, extractPreq([course], course, graph)[0])
        # if no dep, place it
        if len(dependencies):
            # if dep constains last skip it
            for dep in sorted(dependencies, key=lambda x: x[1], reverse=True):
                if(dep[0]=="LAST"):
                    return coursesTaken, planed
            # iterate dependecies depth wise
            lvl = -1
            for dep in sorted(dependencies, key=lambda x: x[1], reverse=True):
                if lvl == -1:
                    lvl = dep[1]
                cc = [c for c, c_ in coursesTaken]
                if dep[0] in cc:
                    continue
                if lvl > dep[1]:
                    lvl = dep[1]
                    plannedmax = max(planlst)
                    planlst = [after]
                if logfile:
                    print("\t"*plandep,"planning course :",dep[0],dep[1],file = logfile)
                ctt, planed = AcadPlanner({dep[0]: extractPreq([dep[0]], dep[0], graph)[0]}, Courseshedule, graph, Sems,
                                          [], coursesTaken, plandep=dep[1], after=plannedmax,logfile=logfile)
                coursesTaken = ctt
                assert (planed is not None)
                planlst.append(planed)

        cc = [c for c, c_ in coursesTaken]
        if course not in cc:
            if logfile:
                print("\t"*plandep,"planning course :",course,f"after => {after}",file = logfile)
            coursesTaken.append((course, plannedmax))
            planed = PlaceCourse(course, Courseshedule, plandep, Sems, max(planlst))

    return coursesTaken, planed

def AcadPlannerLast(courses_plan_dict, Courseshedule, Sems, courses_to_take,coursesTaken=None,logfile=None):
    if not coursesTaken:
        coursesTaken = list()
    planed = None
    yr = max(Sems)
    sem = 0
    print(Sems)
    for s in Sems[yr]:
        if len(Sems[yr][s]):
            sem = s
    
    sem = SemCodedict[0][sem]
    print(yr,sem)
    plannedmax = (yr,sem)
    for course in sorted(courses_plan_dict, key=lambda x: sorter(courses_plan_dict[x]), reverse=True):
        dependencies = courses_plan_dict.get(course, [])
        if len(dependencies) == 1:
            for dep in sorted(dependencies, key=lambda x: x[1], reverse=True):
                if(dep[0]=="LAST"):
                    print("placing last")
                cc = [c for c, c_ in coursesTaken]
                if course not in cc:
                    if logfile:
                        print("planning course :",course,f"after => {plannedmax}",file = logfile)
                    coursesTaken.append((course, plannedmax))
                    planed = PlaceCourse(course, Courseshedule, 0, Sems, plannedmax,noincr=True)



SemCodedict = [{"Fa": 0, "Sp": 1, "Su": 2}, {0: 'Fa', 1: 'Sp', 2: 'Su'}]


def PlaceCourse(course, CourseSchedule, isdependency, Sems, after,noincr=False):
    """
    course: course name
    CourseSchedule: dictionary mapping course names to a list of semesters in which they are available
    isdependency: boolean indicating whether the course is a dependency
    Sems: plan of the semesters assigned with courses, where planned course details are updated
    after: semester from which we are planning
    """
    planned = None
    earliest_available = None
    # Check if the course is a dependency
    # Find the earliest available semester for the dependency course
    earliest_available = getEarliestAvailableSem(course, CourseSchedule, after,noincr)
    year, sem = earliest_available
    if year not in Sems:
        Sems[year] = newAcademicYr()
    Sems[year][SemCodedict[1][sem]].append(course)
    planned = earliest_available

    return planned


def incAfter(after):
    year, semCode = after
    semCode += 1
    if semCode > 2:
        semCode %= 3
        year += 1
    return (year, semCode)


def getEarliestAvailableSem(course, CourseSchedule, after,noincr=False):
    if not noincr:
        after = incAfter(after)
    courseAvail = CourseSchedule[course]
    # ##print()
    SemCodedict = {"Fa": 0, "Sp": 1, "Su": 2}, {0: 'Fa', 1: 'Sp', 2: 'Su'}
    courseAvailCode = [
        SemCodedict[0][i] for i in courseAvail
    ]
    while True:
        year, semCode = after
        sem = SemCodedict[1][semCode]
        if sem not in courseAvail:
            after = incAfter(after)
        else:
            return after
