#!/usr/bin/env python
#Filename: last_logon.py
#Written for Python 2.7
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/91/2016
#Email: charles.frank@trojans.dsu.edu
#
#USAGE: 
#usage: last_logon.py [-h] [-p <PATTERN>] [-s <STARTING>] [-e <ENDING>] [-l]
#                     [-n] [-t]
#
#DSU Linux User Last Logon Script
#
#optional arguments:
#  -h, --help     show this help message and exit
#  -p <PATTERN>   PATTERN for class
#  -s <STARTING>  STARTING from student number
#  -e <ENDING>    ENDING with student number
#  -l             Last Logon of students
#  -n             Total Number of Logons
#  -t             Total Amount of Logon Time per student
#  -y             Since date
#  -z             To date

import read_ini

#Generates a file name
def generate_filename() :
    a_file = read_ini.read_ini_parameter("LastLogon")['tmpdir'] 
    a_file = a_file + read_ini.read_ini_parameter("LastLogon")['rptname']
    return a_file
#
#Main routine:
#
#    import necessary modules
#
#    parse out the command line arguments
#


if __name__ == "__main__":
    import cgi, cgitb
    import argparse
    import subprocess
    import datetime
    import time
    import socket
    import last_logon
    import email_rpt
    import os
    

    # Parse out the various options provided

    parser = argparse.ArgumentParser(description="DSU Linux User Last Logon Script")

    parser.add_argument("-p",
                        dest="student_pattern",
                        default="*",
                        help="PATTERN for class",
                        metavar="<PATTERN>")
    parser.add_argument("-s",
                        dest="student_starting",
                        default=1,
                        type=int,
                        help="STARTING from student number",
                        metavar="<STARTING>")
    parser.add_argument("-e",
                        dest="student_ending",
                        default=99,
                        type=int,
                        help="ENDING with student number",
                        metavar="<ENDING>")
    parser.add_argument("-l",
			action='store_true',
                        help="Last Logon of students")
    parser.add_argument("-n",
			action='store_true',
                        help="Total Number of Logons")
    parser.add_argument("-t",
			action='store_true',
                        help="Total Amount of Logon Time per student")
    parser.add_argument("-y",
                        dest="starting_date",
                        default="20160101000000",
                        help="Starting Date",
                        metavar="<STARTING_DATE>")
    parser.add_argument("-z",
                        dest="ending_date",
                        default="29991231000000",
                        help="Ending Date",
                        metavar="<ENDING_DATE>")

    #get the arguments
    args = parser.parse_args()

    #If the command line option was chosen
    #for the last logon information
    if (args.l or args.n or args.t) :
        
        #get the student list
        student_list = []
        student_list = last_logon.get_student_list(args.student_pattern,
                                                   args.student_starting,
                                                   args.student_ending)

        #set the standard out to a file name
        file_name = generate_filename()

        #call last logon report
        last_logon.display_last_logon(student_list,
				      args.l,
				      args.n,
				      args.t,
                                      args.starting_date,
                                      args.ending_date,
                                      file_name)

        #email the last logon report
        email_rpt.email_last_logon(file_name)


  
        

        

    

    

    

    

