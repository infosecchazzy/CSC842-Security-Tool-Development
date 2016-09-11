#!/usr/bin/env python 
#Filename: display_last.py
#Written for Python 2.7
#IDEA:
#
#This script was requested by Prof. Thomas Havlversion of DSU
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 09/09/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#
#    This script will display the last logon for Linux ids in HTML
#    that are associated with students in a particular class.
#
#   Called by last_stud.py
#    
#POST PARAMETERS:
#
#   f_class         Class
#   f_starting      Starting with student
#   f_ending        Ending with Student
#   last_report      Last Logon report requested
#   num_logins      Number of logins requested
#   total_time      Total Time Requested
#
#Pseudocode:
#
#    Parse the post arguments
#
#    Generate the list of students
#
#    Depending upon the post options:
#        
#        Display the last logon for the students in the list
#        Display total number of logins
#        Display total amount of time  
#

import subprocess
import datetime
import time
import socket
import cgi, cgitb
    
#
#Function:
#    month_converter - Returns the numeric value of the abbreviated Month
#
#Parameter:
#    month - Abbreviated string Value of the month
#
#Returns:
#    Index + 1 of the array of abbreviated months

def month_converter(month) :
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

#
#Function:
#    get_student_list - contructs a list of unix ids based upon parameters
#
#Parameter:
#    s_pattern - the starting pattern of the Linux id.  This is the DSU class designation.
#
#    s_starting - a number representing the starting range for the Linux id.  The DSU student number.
#
#    s_ending - a number reresenting the ending range for the Linux id.  The DSU student number.
#
#Pseudocode:
#    set an empty list s_list
#
#    for i in range s_starting to and including s_ending
#        login_id = s_pattern + i
#        Add login_id to s_list
#
#    return s_list
#
#Returns:
#    A list (s_list) of student ids based upon the parameters
#
#Example:
#    s_pattern = p5
#    s_start = 1
#    s_end = 12
#
#    s_list = [p501, p502, ..... , p511, p512]

def get_student_list(s_pattern, s_starting, s_ending) :

    #define an empty list
    s_list = []

    #make sure starting is less than ending
    if s_starting > s_ending :
        tmp = s_starting
        s_starting = s_ending
        s_ending = s_starting
        
    #go from the starting to the ending 
    for i in range(s_starting, (s_ending + 1)) :

        #assign student number
        student_num = str(i)

        #format the number if necessary
        if ( len(student_num) == 1 ) :
            student_num = "0" + student_num

        #create student id
        login_id = s_pattern + student_num 

        #add login_id to the list
        s_list.append(login_id)

    #return the list with login ids
    return s_list

#
#Function:
#    display_last_logon - produces the last logon report
#
#Parameter:
#    s_list - list of student Linix ids
#
#    flag_l - flag to determine prining the first line from the Linux last command for each student id
#
#    flag_n - flag to determine printing the number of logons from the Linux last command for each student id
#
#    flag_t - flag to determine prining the total time from the Linux last command for each student id
#
#Linux Command:
#
#      last - this Linux command will display the logon information for the Linux system
#
#
#Pseudocode:
#    
#      Call the last Linux command for the student ids in s_list
#    
#      if (flag_l)    
#          display the first line of logon information from the last command for the student
#
#      if (flag_n)
#          display the number of entries for the student 
#              
#      if (flag_t)
#          display the total amount of time for each student
#Returns:
#      N/A
#
#Example:
#    s_list = [p501, p502, ..... , p529, p530]
#    flag_l = true
#    flag_n = true
#    flag_t = true
#
#    % last p501
#          p501     pts/11       138.247.149.21   Thu Mar 24 19:42   still logged in
#          p501     pts/14       138.247.149.21   Thu Mar 24 09:37 - 09:41  (00:04)
#          p501     pts/20       138.247.99.195   Thu Mar 24 07:07 - 08:08  (01:01)
#
#  Last Logon report:
#          p501     pts/11       138.247.149.21   Thu Mar 24 19:42   still logged in
#          Number of logins for p501: 3
#          Amount of time (minutes) for p501: 3.20
#    

def display_last_logon(s_list, flag_l, flag_n, flag_t) :

    now = datetime.datetime.now()

    #display results to html page

    print "Content-type:text/html\r\n\r\n"
    print """
    <html>
    <h1>DISPLAY LAST LOGON MONITOR RESULTS</h1>
    <head>
    <style>
    table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }

    td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
    }

    tr:nth-child(even) {
    background-color: #dddddd;
    }
    </style>
    </head>
    """
    print "<body>"
    print "Date/Time: " + now.strftime("%Y-%m-%d %H:%M") + "<br>"
    print "<br>"

    #Simple Table Header
    if flag_l or flag_n or flag_t :
        print "<table>"
        print "<tr>"
        print "<th>LAST ACTIVITY RESULTS</th>"
        print "</tr>"
    
    #contain the list of users who have not logged in
    no_logins = []

    #contain the number of logons for each user
    student_logins = []

    #contain student total time
    student_total_time = []

    #the wtmp message line at the end of the last command
    wtmp_line = ""

    #create table
    #print "<tr>"
    
    #go thru each student id in the list
    for linux_id in s_list :

        #construct last command and grep for the student id
        linux_cmd = "last -Fd " + linux_id 

        #open a process with the linux command
        p = subprocess.Popen(linux_cmd, stdout=subprocess.PIPE, shell=True)

        #assign the output for the command
        (output, err) = p.communicate()

        #wait for the command to complete
        p_status = p.wait()

        #split the output into individual lines
        each_output_line = output.splitlines()

        #initialization
        total_seconds = 0
        num_logins = 0
        total_time = 0
        first_line = True

        #go thru each line of output from the last command for the linux_id
        for a_line in each_output_line:

            #strip whitespace from the line
            a_line = a_line.strip()

            #linux id did not log on
            #blank line
            if len(a_line) == 0 :
                if flag_l and first_line :
                    no_logins.append(linux_id)
                first_line = False
            #wtmp message
            elif "wtmp begins" in a_line :
                wtmp_line = a_line

            #now we have time to report
            else :

                #there is an entry for the linux id
                #report on the latest entry from the last command if flag_l set
                if first_line  :
                    if flag_l :
                        print "<tr>"
                        print "<td>" + a_line + "</td>"
                        print "</tr>"
                    first_line = False

                #logon found, increment
                num_logins = num_logins + 1

                #split the line into its various fields
                each_field = a_line.split()

                #get todays date and current time
                d = datetime.datetime.now()
                curr_time = datetime.datetime(d.year,
                                              d.month,
                                              d.day,
                                              d.hour,
                                              d.minute,
                                              d.second)

                #last logon reporting user still logged in
                if  "still logged in" in a_line :

                    # get the month,day,time from the output of last command                   
                    month = month_converter(each_field[4])
                    day = each_field[5]
                    year = each_field[7]
            
                    #HH:MM:SS
                    time = each_field[6]
                    h_m_s = time.split(":")
        

                    #calculate the last_logon_time
                    last_logon_time =  datetime.datetime(int(year), 
                                                         int(month), 
                                                         int(day),
                                                         int(h_m_s[0]), 
                                                         int(h_m_s[1]), 
                                                         int(h_m_s[2]))

                                  
                    #calculate difference                    
                    diff_time = (curr_time - last_logon_time).total_seconds()

                    #keep running total                   
                    total_time = total_time + diff_time
                    
                else :

                    #determine where the time is on the last line
                    if "crash" not in a_line and "down" not in a_line :
                        timestamp = each_field[14]
            
                    else  :
                        timestamp = each_field[10]

                    #hour and minutes
                    mm = timestamp[1:3]
                    ss = timestamp[4:6]

                    #calculate the time
                    #Hours                    
                    last_logon_time = (int(mm) * 60)  
                    #Add seconds                      
                    last_logon_time =  last_logon_time + int(ss)

                    #keep running total             
                    total_time = total_time + last_logon_time 

                                           
        #linux id has entries in output from last command
        if linux_id not in no_logins :

            #flag turned on for number of entries
            if flag_n :
                student_logins.append("Number of Logins for " + linux_id + ": " + '%5d' % num_logins)

            #flag turned on for total time               
            if flag_t :
                #divide by 60 to get minutes
                tt_min = total_time / 60.0

                student_total_time.append("Total time logged in for " + str(linux_id) + ": " + '%8.2f' % tt_min)

        #linux id did not log on
        if first_line :
            if flag_l :
                no_logins.append(linux_id)

    #Display when wtmp begins
    if flag_l or flag_n or flag_t :
        
        print "<td>" + wtmp_line + "</td>"

        #end the table
        print "</tr>"
        print "</table>"
    

    #Display number of logins for users

    if flag_n :

        print "<br>"
        print "<table>"
        print "<tr>"
        print "<th>NUMBER OF LOGINS RESULTS</th>"
        print "</tr>"

        for a_line in student_logins :
            print "<tr>"
            print "<td>" + a_line + "</td>"
            print "</tr>"
            
        print "</table>"
        

    #Display total_time
    if flag_t :

        print "<br>"
        print "<table>"
        print "<tr>"
        print "<th>TOTAL TIME RESULTS (MINUTES)</th>"
        print "</tr>"

        for a_line in student_total_time :
            print "<tr>"
            print "<td>" + a_line + "</td>"
            print "</tr>"

        print "</table>"

    #Display all users who have not logged in
    if flag_l or flag_n or flag_t :
        first_time = True
        for linux_id in no_logins :

            if first_time :
                print "<br>"
                print "<table>"
                print "<tr>"
                print "<th>NEVER LOGGED ON RESULTS</th>"
                print "</tr>"
                first_time = False

            print "<tr>"
            print "<td>" + linux_id + "</td>"
            print "</tr>"
        
        print "</table>"
            
    print "</body>"
    print "</html>"

    return

#
#Main routine:
#
#    
#    parse out the post commands
#
#    get the student list
#
#    call the last logon report
#
#    call the monitoring function
#

#show any errors to the browser
cgitb.enable()

#Create instance of FieldStorage 
form = cgi.FieldStorage()

#Get data from fields
pattern = str(form.getvalue('f_class'))
starting  = int(form.getvalue('f_starting'))
ending  = int(form.getvalue('f_ending'))

if form.getvalue('last_report') :
    l_flag = True
else :
    l_flag = False

if form.getvalue('num_logins') :
    n_flag = True
else :
    n_flag = False

if form.getvalue('total_time') :
    t_flag = True
else :
    t_flag = False

#flip flop if necessary
if starting > ending :
    tmp = ending
    ending = starting
    starting = tmp

#get student list
student_list = []
student_list = get_student_list(pattern, starting, ending)

#call display logon with parameters
display_last_logon(student_list, l_flag, n_flag, t_flag)



        

    

    

    

    

