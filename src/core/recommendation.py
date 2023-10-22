from networkx import DiGraph


def has_prerequisites(course: str, graph: DiGraph):
    if graph.has_node(course):
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
        
def cleanCourseCode(coursesRaw:list):
    courses = []
    for course in coursesRaw:
        course = course if "*" not in course else course[:course.find("*")]
        course = course.strip()
        course = " ".join(course.split());
        courses.append(course)
    return courses

def newAcademicYr(): 
    semester_dict= {"Fa":list().copy(),"Sp":list().copy(),"Su":list().copy()}
    return semester_dict
    

def sorter(deps):
    if(not deps): return -1;
    depth = 0
    print(deps)
    for code,crsdepth in deps:
        depth =max(depth,crsdepth)
    return depth

def extractPreq(courses_to_take,course, graph,lvl=0):
    dependencies = []
    print(f"\n\n\nchecking prerequesites for {course}")
    if has_prerequisites(course, graph):
        preqCourses = get_prerequisites(course, graph)
        print(preqCourses)
        for preq in preqCourses:
            if preq is not None:
                if preq not in courses_to_take:
                    courses_to_take.append(preq)
                dependencies.append((preq,lvl))
                print(f"dependenices Now",dependencies)
                if has_prerequisites(preq, graph):
                    dep_in_depth,crsestake_indpth = extractPreq(courses_to_take,preq, graph,lvl+1)
                    dependencies.extend(dep_in_depth)
                    courses_to_take = crsestake_indpth
    return dependencies,courses_to_take
def generate_degree_plan(text: dict, graph: DiGraph, Courseshedule:dict=None):
    courses_to_take = []

    courses_plan_dict = {}
    # run a loop over all the keys of courses that have to be taken
    for key in text.keys():
        # extract courses for each key
        coursesRaw = text[key]
        counter = 0
        limit = 0
        courses = cleanCourseCode(coursesRaw)
        for course in courses:
            dependencies = []
            if "SELECT".lower() in course.lower():
                # if there is a selection criteria, set it as a limit
                limit = int(course.split(" ")[1].strip())
            if limit > 0 and counter == limit:
                # if the selection criteria has been satisfied break the inner loop
                break
            if "SELECT".lower() not in course.lower():
                original_course = course
                print(f"||{course}||is having pre requesite" if has_prerequisites(course, graph) else f"||{course}|| no preq")
                dependencies,courses_to_take = extractPreq(courses_to_take,original_course, graph)
                print(dependencies)
                courses_plan_dict[original_course] = dependencies
                if original_course not in courses_to_take: courses_to_take.append(original_course)
                counter = counter + 1
    # return courses_to_take,courses_plan_dict
    Sems = {1:newAcademicYr(),2:newAcademicYr()}


    for course in sorted(courses_plan_dict,key=lambda x:sorter(courses_plan_dict[x]),reverse=True):
        print(f'{course} dependeinces:\t\t\t:',end=" ")
        for dep in courses_plan_dict[course]:
            print(f'\t\t{dep}',end="")
        print()
    
    print("stating acad planner",f"for {len(courses_to_take)}, {len(set(courses_to_take))}")
    print(*courses_to_take,sep="\t")
    coursesTaken,planned=AcadPlanner(courses_plan_dict,Courseshedule,graph,courses_to_take,Sems)
    for crs in courses_to_take:
        if crs not in coursesTaken:
            print(crs,"Not taken why why")

    print("stating acad planner",f"for {len(courses_to_take)}, {len(set(courses_to_take))}")
    print(*courses_to_take,sep="\t")
    print("stating acad planner",f"for {len(coursesTaken)}, {len(set(coursesTaken))}")
    print(*coursesTaken,sep="\t")

def AcadPlanner(courses_plan_dict,Courseshedule,graph,Sems,courses_to_take,coursesTaken=None,plandep=0,after=None):
    if(not coursesTaken): coursesTaken=list()
    for course in sorted(courses_plan_dict,key=lambda x:sorter(courses_plan_dict[x]),reverse=True):
        plannedmax=None
        dependencies = courses_plan_dict.get(course, extractPreq([course],course,graph)[0])
        # if no dep, place it
        if(len(dependencies)):
            # iterate dependecies depth wise
            for dep in sorted(dependencies,key=lambda x : x[1],reverse=True):
                print(f"planning {course} with {dep}")
                ctt,planed = AcadPlanner({dep[0]:extractPreq([dep[0]],dep[0],graph)[0]},Courseshedule,graph,Sems,coursesTaken,plandep=1,after=after)
                coursesTaken.extend(ctt)
        
        if course in coursesTaken:
            print(f"Already placed")
            continue
        planed=coursesTaken.append((course,plannedmax))
        PlaceCourse(course,Courseshedule,plandep,Sems,after)
        print(f"{course} is being placed")
        
    return coursesTaken,planed
    

def PlaceCourse(course,Courseshedule,isdependency,Sems,after):
    """
    course:coursename
    Courseshedule:dictinoray <coursename:listof semesters in which available
    is dependnecy : says it is dependecy so earliest posible sem to be assigned after given sem
    Sems: plan of the sems asiigned with courses, where plancourse detail is updated
    after:semester from which we are planning 
    """
    planned=None
    return planned

def generate_degree_plan_phase1(text: dict, graph: DiGraph, Courseshedule:dict=None):
    courses_to_take = []
    # run a loop over all the keys of courses that have to be taken
    for key in text.keys():
        # extract courses for each key
        coursesRaw = text[key]
        counter = 0
        limit = 0
        courses = cleanCourseCode(coursesRaw)
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
