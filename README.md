# SmartClassPlanningTool

https://colab.research.google.com/drive/1a7jT5Uh_1r0OMFzWhxJUS-eBm6mX0JVJ#scrollTo=JbDK4M00mjiq 

Please use the following command to run the program:
```
python3 -m venv env #[optional]

source env/bin/activate

pip install -r requirements.txt

cd src/

python3 src/console.py 

#enter file paths as per asked
# "Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf" 
#"Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq3.json" 
#"Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json" 
# "Plan1file"
#check the file from src/ folder or as per given file path

```

---
---

### Usage of console.py 
```
usage: console.py  

Process some files.

Std Input arguments:
Feature 1
  f1          Path to the first file [Degree Works]
  f2          Path to the second file [Prerequisite Graph]
  f3          Path to the third file [Class Schedule]
  file        Path to the results
Feature 2
  f3          Path to the third file [Class Schedule]
  f2          Path to the second file [Prerequisite Graph]

```
---
Functionalities of feature 1:

1) Input parsing => 3 inputs

2) Main Logic level 1 => looping the courses that need to be taked must


3) Main logic level 2 => remaining residual that need to be met like optional to schedule


4) Excel sheet Generation
---

---
Functionalities of feature 2:

1) Input parsing => 2 inputs

2) Main Logic level 1 => looping the courses that are in schedule one by one


3) Main logic level 2 => validate course is followed after all its requesites are covered


4) print our results
---

Guide to do the test cases

Use the command python -m unittest discover -v to discover and execute all the tests.
Use the command python -m unittest test_package.test_module -v to run a single test module.
Use the command python -m unittest test_package.test_module.TestClass -v to run a single test class.
Use the command python -m unittest test_package.test_module.TestClass.test_method -v to run a single test method.

```
python3 -m unittest discover -v
python3 -m coverage run -m unittest
python3 -m coverage report
python3 -m coverage html 
```