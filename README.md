# SmartClassPlanningTool

## Purpose

This document describes how to set up and use the SmartClassPlanningTool
application to get the complete course plan for a student and determine
whether the existing course plan has any prerequisite issues

The Academic Course Planner and Validator is a comprehensive tool designed for students and academic advisors. It assists in planning academic courses for a degree, ensuring that all prerequisites are met and schedules are feasible. The system can generate semester-wise course plans and validate existing schedules against prerequisites.



## Prerequisites

### Supported Platforms

SmartClassPlanningTool has been tested on Windows 10 and 11  operating 
systems

### Required Software

___
#### USER  :
There is no additional software required to run the program on Windows
#### Developer :

Before using the Academic Course Planner and Validator, ensure you have the following prerequisites:
Python 3.8+: The software is written in Python and requires Python 3.8 or higher.
Required Python Libraries: Install necessary libraries such as networkx, pandas, openpyxl, and pdfminer.six. Use the command pip install networkx pandas openpyxl pdfminer.six.
PDF Reader: A PDF reader is needed to view output files if not using Excel.
___



## Download

To get the SmartClassPlanningTool, please visit https://github.com/Team3CSU/SmartClassPlanningTool

#### Executable file :
Go to page : https://github.com/Team3CSU/SmartClassPlanningTool/tree/main/dist
Click on "consolenew.exe" and download it to get executable file to run on windows.

### Get Sample Inputs and  source code [for developers need only]
Navigate to https://github.com/Team3CSU/SmartClassPlanningTool

You can get the Source code, executable files,sample input files by clicking on "Code" followed by "Download ZIP"

## Installation

This software does not require any installation. Simple run the consolenew.exe
file provided in dist folder to use the application

## Usage

To use SmartClassPlanning tool, navigate to the dist folder and run consolenew.exe.
You will be greeted by a menu. Please provide the number of
the feature you want to use or input 3 and press enter to exit the program

To generate class plan provide 1 as input. You would be asked to provide 3 
input files. If no location is provided for the files, the software would pick the 
default location which is displayed in the terminal. The first input file is degree 
works which should be a pdf file. Provide the location of the file and press enter 
to proceed to the next step. Second input file is the prerequisite graph which 
should be a json file and the third input file is course schedule which should be 
a json file as well. Once all the input files are provided, the user would have to 
provide the name of the output file that would be stored on the computer. 
Provide the file name and press enter and the output file would be generated in the 
same folder.

To check prerequisite issues of a course plan, please provide 2 as input. You 
would be asked to provide 2 input files. If no location is provided, the software 
would pick the default location which is displayed in the terminal. The first input 
file is the prerequisite graph which should be a json file. Provide the location of 
the file and press enter to proceed to the next step. Second input file is course 
plan file which should be an xlsx file. Once the two input files are provided, the 
result would be generated on the terminal indicating whether the course plan 
has any prerequisite issues or notx