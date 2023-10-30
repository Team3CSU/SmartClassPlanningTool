# SmartClassPlanningTool

https://colab.research.google.com/drive/1a7jT5Uh_1r0OMFzWhxJUS-eBm6mX0JVJ#scrollTo=JbDK4M00mjiq 

Please use the following command to run the program:
```
python3 -m venv env #[optional]

source env/bin/activate

pip install -r requirements.txt

cd src/

python3 console.py "../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/Sample Input2.pdf" "../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/preReq3.json" "../Software Design Development Section V01 Fall Semester 2023 CO - 10102023 - 1004 AM/courseSchedule.json" "Plan1file"

#check the file from src/ folder or as per given file path

```

---
---

### Usage of console.py 
```
usage: console.py [-h] f1 f2 f3 file

Process some files.

positional arguments:
  f1          Path to the first file [Degree Works]
  f2          Path to the second file [Prerequisite Graph]
  f3          Path to the third file [Class Schedule]
  file        Path to the results

options:
  -h, --help  show this help message and exit
```
---
---
Functionalities:

1) Input parsing => 3 inputs
> 1 credit filter out other courses and take only first non pre-requisite course

2) Main Logic level 1 => looping the courses that need to be taked must


3) Main logic level 2 => remaining residual that need to be met like optional to schedule


4) Excel sheet Generation
---
---
