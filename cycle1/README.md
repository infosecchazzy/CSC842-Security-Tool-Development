Filename: 
    last_logon.py
Written:
    for Python 2.7
IDEA:

This script was requested by Dr. Thomas Halverson of DSU

AUTHOR:
    Charles V. Frank Jr.
Date:
    08/25/2016
Email: 
    charles.frank@trojans.dsu.edu

DESCRIPTION:

    This script will display the last logon for Linux ids
    that are associated with students in a particular class.
    
    Lastly, this script can monitor the activity of the Linux ids/Students.

Pseudocode:

    Parse the command line options

    Generate the list of students

    Depending upon the command line options chosen:
        
        Display the last logon for the students in the list

        Monitor the activities of the students

USAGE: 
usage: last_logon.py [-h] [-p <PATTERN>] [-s <STARTING>] [-e <ENDING>] [-l]
                     [-n] [-t] [-m]

DSU Linux User Last Logon Script

optional arguments:
  -h, --help     show this help message and exit
  -p <PATTERN>   PATTERN for class
  -s <STARTING>  STARTING from student number
  -e <ENDING>    ENDING with student number
  -l             Last Logon of students
  -n             Total Number of Logons
  -t             Total Amount of Logon Time per student
  -m             Monitor student activity

EXAMPLES:    

    linux_logon.py -p p5 -s 0 -e 10 -l -n -t

        for students [p500 ... p510] produce the last logon report
        including number of logons and total time

    linux_logon.py -p p5 -s 0 -e 10 -l 

        for students [p500 ... p510] produce the last logon report
        excluding number of logons and total time

    linux_logon.py -p p5 -s 0 -e 10 -m

        for students [p500 ... p510], monitor thier activity
    
