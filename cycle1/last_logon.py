#!/usr/bin/env python
##Filename: last_logon.py
##Written for Python 2.7
##IDEA:
##
##This script was requested by Prof. Thomas Havlversion of DSU
##
##AUTHOR:
##    
##Charles V. Frank Jr.
##Date: 08/25/2016
##Email: charles.frank@trojans.dsu.edu
##
##DESCRIPTION:
##
##    This script will display the last logon for Linux ids
##    that are associated with students in a particular class.
##    
##    Lastly, this script can monitor the activity of the Linux ids/Students.
##
##Pseudocode:
##
##    Parse the command line options
##
##    Generate the list of students
##
##    Depending upon the command line options chosen:
##        
##        Display the last logon for the students in the list
##
##        Monitor the activities of the students
##
##USAGE: 
##usage: last_logon.py [-h] [-p <PATTERN>] [-s <STARTING>] [-e <ENDING>] [-l]
##                     [-n] [-t] [-m]
##
##DSU Linux User Last Logon Script
##
##optional arguments:
##  -h, --help     show this help message and exit
##  -p <PATTERN>   PATTERN for class
##  -s <STARTING>  STARTING from student number
##  -e <ENDING>    ENDING with student number
##  -l             Last Logon of students
##  -n             Total Number of Logons
##  -t             Total Amount of Logon Time per student
##  -m             Monitor student activity
##
##EXAMPLES:    
##
##    linux_logon.py -p p5 -s 0 -e 10 -l -n -t
##
##        for students [p500 ... p510] produce the last logon report
##        including number of logons and total time
##
##    linux_logon.py -p p5 -s 0 -e 10 -l 
##
##        for students [p500 ... p510] produce the last logon report
##        excluding number of logons and total time
##
##    linux_logon.py -p p5 -s 0 -e 10 -m
##
##        for students [p500 ... p510], monitor thier activity
##    
##    
    
##
##Function:
##    month_converter - Returns the numeric value of the abbreviated Month
##
##Parameter:
##    month - Abbreviated string Value of the month
##
##Returns:
##    Index + 1 of the array of abbreviated months

def month_converter(month) :
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

##
##Function:
##    get_student_list - contructs a list of unix ids based upon parameters
##
##Parameter:
##    s_pattern - the starting pattern of the Linux id.  This is the DSU class designation.
##
##    s_starting - a number representing the starting range for the Linux id.  The DSU student number.
##
##    s_ending - a number reresenting the ending range for the Linux id.  The DSU student number.
##
##Pseudocode:
##    set an empty list s_list
##
##    for i in range s_starting to and including s_ending
##        login_id = s_pattern + i
##        Add login_id to s_list
##
##    return s_list
##
##Returns:
##    A list (s_list) of student ids based upon the parameters
##
##Example:
##    s_pattern = p5
##    s_start = 1
##    s_end = 12
##
##    s_list = [p501, p502, ..... , p511, p512]

def get_student_list(s_pattern, s_starting, s_ending) :

    ##define an empty list
    s_list = []

    ##make sure starting is less than ending
    if s_starting > s_ending :
        tmp = s_starting
        s_starting = s_ending
        s_ending = s_starting
        
    ##go from the starting to the ending 
    for i in range(s_starting, (s_ending + 1)) :

        ##assign student number
        student_num = str(i)

        ##format the number if necessary
        if ( len(student_num) == 1 ) :
            student_num = "0" + student_num

        ##create student id
        login_id = s_pattern + student_num 

        ##add login_id to the list
        s_list.append(login_id)

    ##return the list with login ids
    return s_list

##
##Function:
##    display_last_logon - produces the last logon report
##
##Parameter:
##    s_list - list of student Linix ids
##
##    flag_l - flag to determine prining the first line from the Linux last command for each student id
##
##    flag_n - flag to determine printing the number of logons from the Linux last command for each student id
##
##    flag_t - flag to determine prining the total time from the Linux last command for each student id
##
##Linux Command:
##
##      last - this Linux command will display the logon information for the Linux system
##
##      grep - search for patterns
##
##Pseudocode:
##    
##      Call the last Linux command for the student ids in s_list
##    
##      if (flag_l)    
##          display the first line of logon information from the last command for the student
##
##      if (flag_n)
##          display the number of entries for the student 
##              
##      if (flag_t)
##          display the total amount of time for each student
##Returns:
##      N/A
##
##Example:
##    s_list = [p501, p502, ..... , p529, p530]
##    flag_l = true
##    flag_n = true
##    flag_t = true
##
##    % last p501
##          p501     pts/11       138.247.149.21   Thu Mar 24 19:42   still logged in
##          p501     pts/14       138.247.149.21   Thu Mar 24 09:37 - 09:41  (00:04)
##          p501     pts/20       138.247.99.195   Thu Mar 24 07:07 - 08:08  (01:01)
##
##  Last Logon report:
##          p501     pts/11       138.247.149.21   Thu Mar 24 19:42   still logged in
##          Number of logins for p501: 3
##          Amount of time (minutes) for p501: 3.20
##    

def display_last_logon(s_list, flag_l, flag_n, flag_t) :

    ##Header info for the report 
    print("Last Logon Report: \n")
    hostname = socket.gethostname()
    print("Host: " + hostname)
    curr_time = datetime.datetime.now()
    print("Date/Time: " + str(curr_time))
    print("")

    ##contain the list of users who have not logged in
    no_logins = []

    ##contain the number of logons for each user
    student_logins = []

    ##contain student total time
    student_total_time = []

    ##the wtmp message line at the end of the last command
    wtmp_line = ""

    ##go thru each student id in the list
    for linux_id in s_list :

        ##construct last command and grep for the student id
        linux_cmd = "last -Fd " + linux_id 

        ##open a process with the linux command
        p = subprocess.Popen(linux_cmd, stdout=subprocess.PIPE, shell=True)

        ##assign the output for the command
        (output, err) = p.communicate()

        ##wait for the command to complete
        p_status = p.wait()

        ##split the output into individual lines
        each_output_line = output.splitlines()

        ##initialization
        total_seconds = 0
        num_logins = 0
	total_time = 0
	first_line = True

        ##go thru each line of output from the last command for the linux_id
        for a_line in each_output_line:

            ##strip whitespace from the line
            a_line = a_line.strip()

            ##linux id did not log on
            ##blank line
            if  len(a_line) == 0 :
                if flag_l and first_line :
                    no_logins.append(linux_id)
		first_line = False
	    ##wtmp message
	    elif  "wtmp begins" in a_line :
		wtmp_line = a_line

            ##now we have time to report
            else :

                ##there is an entry for the linux id
                ##report on the latest entry from the last command if flag_l set
                if first_line  :
                    if flag_l :
                        print(a_line)
                    first_line = False

                ##logon found, increment
                num_logins = num_logins + 1

                ##split the line into its various fields
                each_field = a_line.split()

                ##get todays date and current time
                d = datetime.datetime.now()
                curr_time = datetime.datetime(d.year,
                                              d.month,
                                              d.day,
                                              d.hour,
                                              d.minute,
                                              d.second)

                ##last logon reporting user still logged in
                if  "still logged in" in a_line :

                    ## get the month,day,time from the output of last command                   
                    month = month_converter(each_field[4])
                    day = each_field[5]
		    year = each_field[7]
		    
                    ##HH:MM:SS
                    time = each_field[6]
		    h_m_s = time.split(":")
		

                    ##calculate the last_logon_time
                    last_logon_time =  datetime.datetime(int(year), 
							 int(month), 
                                                         int(day),
					                 int(h_m_s[0]), 
                                                         int(h_m_s[1]), 
                                                         int(h_m_s[2]))

                                  
                    ##calculate difference                    
                    diff_time = (curr_time - last_logon_time).total_seconds()

                    ##keep running total                   
                    total_time = total_time + diff_time
                    
                else :

                    ##determine where the time is on the last line
                    if "crash" not in a_line and "down" not in a_line :
                    	timestamp = each_field[14]
			
		    else  :
                    	timestamp = each_field[10]

		    ##hour and minutes
                    mm = timestamp[1:3]
                    ss = timestamp[4:6]

		    ##calculate the time
		    ##Hours                    
		    last_logon_time = (int(mm) * 60)  
                    ##Add seconds                      
		    last_logon_time =  last_logon_time + int(ss)

                    ##keep running total             
                    total_time = total_time + last_logon_time 

                                           
        ##linux id has entries in output from last command
        if linux_id not in no_logins :

            ##flag turned on for number of entries
            if flag_n :
                student_logins.append("Number of Logins for " + linux_id + ": " + '%5d' % num_logins)

            ## flag turned on for total time               
            if flag_t :
                ##divide by 60 to get minutes
                tt_min = total_time / 60.0

                student_total_time.append("Total time logged in for " + str(linux_id) + ": " + '%8.2f' % tt_min)

        ##linux id did not log on
        if first_line :
            if flag_l :
                no_logins.append(linux_id)

    ##Display when wtmp begins
    if flag_l or flag_n or flag_t :
    	print("")
    	print(wtmp_line)

    ##Display number of logins for users
    if flag_n :
    	print("")
    	print("Numner of Logins:")
    	for a_line in student_logins :
		print(a_line)

    ##Display total_time
    if flag_t :
    	print("")
    	print("Total Amount of Time (minutes):")
    	for a_line in student_total_time :
		print(a_line)

    ##Display all users who have not logged in
    if flag_l or flag_n or flag_t :
    	print("")
    	print("Never Logged On: ")
    	for linux_id in no_logins :
       		print(linux_id)
                    
    return

##
##Function:
##    display_monitor - monitors student activity
##
##Parameter:
##    s_list - list of student Linix ids
##
##Linux Command:
##
##      w - this Linux command will display usage for users that are logged on
##
##
##Pseudocode:
##    
##      Call the w Linux command for student ids in s_list
##    
##      
##Returns:
##      N/A
##

def display_monitor(s_list) :

    print("Display Monitor: ")

    ##infinite loop
    while True :

	##execte w command for each student	
	for linux_id in s_list:

	        ##construct linux command   
       		linux_cmd = "w -h " + linux_id

        	##open a process with the linux command 
        	p = subprocess.Popen(linux_cmd, stdout=subprocess.PIPE, shell=True)

        	##gather the output from the command
        	(output, err) = p.communicate()

        	##wait for the command to finish
        	p_status = p.wait()

		##split into lines
		lines = output.splitlines()

        	##for each line of the output, print it
        	for a_line in lines :
        		print(a_line)

        ##wait before repeating
        time.sleep(5)

    return
##
##Main routine:
##
##    import necessary modules
##
##    parse out the command line arguments
##
##    get the student list
##
##    call the last logon report
##
##    call the monitoring function
##

if __name__ == "__main__":
    import argparse
    import subprocess
    import datetime
    import time
    import socket


    ## Parse out the various options provided

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
    parser.add_argument("-m",
			action='store_true',
                        help="Monitor student activity")

    ##get the arguments
    args = parser.parse_args()

    ## get student list
    student_list = []
    student_list = get_student_list(args.student_pattern,
                                    args.student_starting,
                                    args.student_ending)

    ##If the command line option was chosen
    ##for the last logon information
    if (args.l or args.n or args.t) :

        display_last_logon(student_list,
				args.l,
				args.n,
				args.t)


    ##If the command line option was chosen
    ##for monitoring students
    if (args.m) :
        
        display_monitor(student_list)
        

        

    

    

    

    

