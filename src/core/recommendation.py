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
        
def cleanCourseCode(coursesRaw:list,Courseshedule):
    courses = []
    for course in coursesRaw:
        course = course if "*" not in course else course[:course.find("*")]
        course = course.strip()
        course = " ".join(course.split());
        if course in Courseshedule:
            courses.append(course)
        else:
            print('{} is missing'.format(course))
            # input()
    return courses

def newAcademicYr(): 
    semester_dict= {"Fa":list().copy(),"Sp":list().copy(),"Su":list().copy()}
    return semester_dict
    

def sorter(deps):
    if(not deps): return -1;
    depth = 0
    ##print(deps)
    for code,crsdepth in deps:
        depth =max(depth,crsdepth)
    return depth

def extractPreq(courses_to_take,course, graph,lvl=0):
    dependencies = []
    ##print(f"\n\n\nchecking prerequesites for {course}")
    if has_prerequisites(course, graph):
        preqCourses = get_prerequisites(course, graph)
        ##print(preqCourses)
        for preq in preqCourses:
            if preq is not None:
                if preq not in courses_to_take:
                    courses_to_take.append(preq)
                dependencies.append((preq,lvl))
                ##print(f"dependenices Now",dependencies)
                if has_prerequisites(preq, graph):
                    dep_in_depth,crsestake_indpth = extractPreq(courses_to_take,preq, graph,lvl+1)
                    dependencies.extend(dep_in_depth)
                    courses_to_take = crsestake_indpth
    return dependencies,courses_to_take
def generate_degree_plan(text: dict, graph: DiGraph, Courseshedule:dict=None):
    courses_to_take = []

    courses_plan_dict = {}
    coursecount = 0
    # run a loop over all the keys of courses that have to be taken
    for key in text.keys():
        # extract courses for each key
        coursesRaw = text[key]
        counter = 0
        limit = 0
        courses = cleanCourseCode(coursesRaw,Courseshedule)
        for course in courses:
            dependencies = []
            if "SELECT".lower() in course.lower():
                # if there is a selection criteria, set it as a limit
                limit = int(course.split(" ")[1].strip())
            if limit > 0 and counter == limit:
                # if the selection criteria has been satisfied break the inner loop
                break
            if "SELECT".lower() not in course.lower():
                coursecount+=1
                original_course = course
                ##print(f"||{course}||is having pre requesite" if has_prerequisites(course, graph) else f"||{course}|| no preq")
                dependencies,courses_to_take = extractPreq(courses_to_take,original_course, graph)
                ##print(dependencies)
                courses_plan_dict[original_course] = dependencies
                if original_course not in courses_to_take: courses_to_take.append(original_course)
                counter = counter + 1
    # return courses_to_take,courses_plan_dict
    Sems = {0:newAcademicYr(),1:newAcademicYr()}
    ##print(Sems)


    for course in sorted(courses_plan_dict,key=lambda x:sorter(courses_plan_dict[x]),reverse=True):
        #print(f'{course} dependeinces:\t\t\t:',end=" ")
        for dep in courses_plan_dict[course]:
            pass
            #print(f'\t\t{dep}',end="")
        #print()
    
    #print("stating acad planner",f"for {len(courses_to_take)}, {len(set(courses_to_take))}")
    #print(*courses_to_take,sep="\t")
    coursesTaken,planned=AcadPlanner(courses_plan_dict,Courseshedule,graph,Sems,courses_to_take,after=(0,-1))
    coursesTaken_c = [c for c, t in coursesTaken]
    for crs in courses_to_take:
        if crs not in coursesTaken_c:
            print(crs,"Not taken why why")
    else:
        print("All Courses placed")

    print("before clean :",coursecount,"courses")
    print("Courses planned to take before scheduling",f"for {len(courses_to_take)}, {len(set(courses_to_take))}")
    print(*courses_to_take,sep="\t")
    print("Courses Scheduled",f"for {len(coursesTaken)}, {len(set(coursesTaken))}")
    print(*coursesTaken,sep="\t")


    print("\n\n\n\n")
    return Sems

def AcadPlanner(courses_plan_dict,Courseshedule,graph,Sems,courses_to_take,coursesTaken=None,plandep=0,after=(0,-1)):
    if(not coursesTaken): coursesTaken=list()
    planed = None
    for course in sorted(courses_plan_dict,key=lambda x:sorter(courses_plan_dict[x]),reverse=True):
        # ##print(f'{course} dependeinces:\t\t\t:',end=" ")
        # for dep in courses_plan_dict[course]:
        #     ##print(f'\t\t{dep}',end="")
        # continue
        plannedmax=after
        planlst = [after]
        dependencies = courses_plan_dict.get(course, extractPreq([course],course,graph)[0])
        # if no dep, place it
        if(len(dependencies)):
            # iterate dependecies depth wise
            lvl = -1
            for dep in sorted(dependencies,key=lambda x : x[1],reverse=True):
                if lvl == -1:lvl = dep[1]
                cc = [c for c,c_ in coursesTaken]
                if dep[0] in cc:
                    ##print(f"Already placed")
                    continue
                if lvl>dep[1]:
                    lvl = dep[1]
                    plannedmax = max(planlst)
                    planlst = [after]
                ##print(f"planning {course} with {dep}")
                ctt,planed = AcadPlanner({dep[0]:extractPreq([dep[0]],dep[0],graph)[0]},Courseshedule,graph,Sems,[],coursesTaken,plandep=1,after=plannedmax)
                coursesTaken=ctt
                assert(planed is not None)
                # plannedmax=max(planed,plannedmax)
                planlst.append(planed)
        
        cc = [c for c,c_ in coursesTaken]
        #print(cc)
        if course not in cc:
            coursesTaken.append((course,plannedmax))
            ##print("\n\n")
            # ##print(planlst)
            # ##print(max(planlst))
            #print(cc)
            #print(coursesTaken)
            #print("planning",course)
            planed = PlaceCourse(course,Courseshedule,plandep,Sems,max(planlst))
            #print(cc)
            #print(coursesTaken)
            #print(Sems)
            #input()
        ##print(f"{course} is being placed")
    

    return coursesTaken,planed
    

SemCodedict= [{"Fa":0,"Sp":1,"Su":2},{0: 'Fa', 1: 'Sp', 2: 'Su'}]
def PlaceCourse(course, CourseSchedule, isdependency, Sems, after):
    ##print(course, CourseSchedule, isdependency, Sems, after)

    """
    course: course name
    CourseSchedule: dictionary mapping course names to a list of semesters in which they are available
    isdependency: boolean indicating whether the course is a dependency
    Sems: plan of the semesters assigned with courses, where planned course details are updated
    after: semester from which we are planning
    """
    planned = None
    earliest_available= None
    # Check if the course is a dependency
    # Find the earliest available semester for the dependency course
    earliest_available = getEarliestAvailableSem(course, CourseSchedule, after)
    year,sem = earliest_available
    if year not in Sems:
        Sems[year]=newAcademicYr()
    # ##print(sem,year,SemCodedict[1][sem])
    # exit()
    # Sems[year][SemCodedict[sem]]
    # ##print(Sems[year][SemCodedict[1][sem]])
    Sems[year][SemCodedict[1][sem]].append(course)
    ##print(Sems)
    # Update the planned course in Sems
    # if earliest_available_sem in Sems:
    #     Sems[earliest_available_sem].append(course)
    # else:
    #     Sems[earliest_available_sem] = [course]
    planned = earliest_available

    return planned

def incAfter(after):
    year,semCode = after
    semCode+=1
    if(semCode>2):
        semCode%=3
        year+=1
    return (year,semCode)

def getEarliestAvailableSem(course, CourseSchedule, after):
    after = incAfter(after)
    courseAvail = CourseSchedule[course]
    # ##print()
    SemCodedict= {"Fa":0,"Sp":1,"Su":2},{0: 'Fa', 1: 'Sp', 2: 'Su'}
    courseAvailCode = [
        SemCodedict[0][i]  for i in courseAvail
    ]
    while True:
        year, semCode = after
        sem= SemCodedict[1][semCode]
        if sem not in courseAvail:
            after = incAfter(after)
        else:
            return after
        

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
                # ##print(f"||{course}||is having pre requesite" if has_prerequisites(course, graph) else f"||{course}|| no preq")
                while has_prerequisites(course, graph):
                    course = get_prerequisite(course, graph)
                    if course is not None and course not in courses_to_take:
                        courses_to_take.append(course)
                if original_course not in courses_to_take: courses_to_take.append(original_course)
                counter = counter + 1
    return courses_to_take
