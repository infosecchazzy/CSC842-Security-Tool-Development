#!/usr/bin/env python 
#Filename: last_logon.py
#Written for Python 2.7
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/02/2016
#Email: charles.frank@trojans.dsu.edu
#
import subprocess
import datetime
import time
import cgi, cgitb
import os
import sys
    
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
#    filename - determines whether to write output to a file
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

def display_last_logon(s_list, flag_l, flag_n, flag_t, filename) :
    
    #show any errors to the browser
    cgitb.enable()

    now = datetime.datetime.now()

    #determine if stdout should be to a file or the screen/browser
    if filename :
        saveout = sys.stdout
        fsock = open(filename, 'w')
        sys.stdout = fsock

    #display results 

    if not filename :
        print "Content-type:text/html\r\n\r\n"

##<script type="text/javascript">
##<code>&lt;a href="javascript:void(0);"<br>&nbsp;onclick="document.execCommand('SaveAs',true,'lastlogon.html');"<br>&nbsp;>Save this report&lt;/a></code>
##</script>
        
    print """
    <!DOCTYPE html>
    <html>
    """

    if not filename :
        print """
        <form action="/cgi-bin/email_existing_llog.py" method="post">
           <input type="submit" name="email" value="email">
        </form>
        """

    print """   
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
    print """
    <script type="text/javascript">
    <code>&lt;a href="javascript:void(0);"<br>&nbsp;onclick="document.execCommand('SaveAs',true,'lastlogon.html');"<br>&nbsp;>Save this report&lt;/a></code>
    </script>
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

    #reset stdout if needed
    if filename:
        sys.stdout = saveout
        fsock.close()

    return

#
#Function:
#    schedule_last_logon - schedule a last logon search
#
#Parameter:
#    s_pattern - the starting pattern of the Linux id.  This is the DSU class designation.
#
#    s_starting - a number representing the starting range for the Linux id.  The DSU student number.
#
#    s_ending - a number reresenting the ending range for the Linux id.  The DSU student number.
#
#    l_flag - last logon report flag
#
#    n_flag - number of logon flag
#
#    t_flag - total amount of time flag
#
#Pseudocode:
#    show the search values
#
#    Select the schedule
#
#    Call cron to schedule the job (creat_cron_last_logon)

def schedule_last_logon(pattern,starting,ending,l_flag,n_flag,t_flag) :

    #display the search information
    #the form will call create_cron_last_logon
    
    print """
    <html>
    <body>
    
    <form action="/cgi-bin/schedule_last_logon.py" method="get">

    <h1>STUDENT LAST LOGON SCHEDULING</h1> 
    Student Range:<br>
    """

    #display the class chosen
    print """
    Class: <input type="text" name="f_class" maxlength = "6"
    """
    print ' value="' + pattern + '"' + " readonly=readonly " +  "><br>"
   
    #display starting student chosen

    print """
    Starting Student: <input type="number" name="f_starting" min=0 max=99
    """
    print ' value="' + str(starting) + '"' + " readonly=readonly " + "><br>"

    #display ending student chosen

    print """
    Ending Student: <input type="number" name="f_ending" min=0 max=99
    """
    print ' value="' + str(ending) + '"' + " readonly=readonly " + "><br>"
    
    print "<br>Reporting Level:<br>"

    #display the check boxes

    #last logon report check box

    if l_flag :
        print """
        <input type="checkbox" name="last_report" value="on" checked disabled /> Last Report
        <input name="last_report" type="hidden" value="true"/>
        """
    else :
        print """
        <input type="checkbox" name="last_report" value="off" disabled /> Last Report
        <input name="last_report" type="hidden" value="false"/>
        """

    #Num logons check box
        
    if n_flag :
        print """
        <input type="checkbox" name="num_logins" value="on" checked  disabled/> Num Logins
        <input name="num_logins" type="hidden" value="true"/>
        """
    else :
        print """
        <input type="checkbox" name="num_logins" value="off"  disabled/>
        <input name="num_logins" type="hidden" value="false"/>
        """

    #Total time check box

    if t_flag :
        print """
        <input type="checkbox" name="total_time" value="off" checked disabled/> Total Time
        <input name="total_time" type="hidden" value="true"/>
        """
    else :
        print """
        <input type="checkbox" name="total_time" value="off" disabled /> Total Time
        <input name="total_time" type="hidden" value="false"/>
        """
    print """
    <br>
    """

    #show radio buttons and input for scheduling
    print """
    <br>
    <p>Scheduling:</p>\
    Time:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="number" name="f_hour" min=0 max=23 value=22>Hour
    &nbsp&nbsp&nbsp<input type="number" name="f_minutes" min=0 max=59 value=0>Minutes
    <br><br>
    <input type="radio" name="frequency" value="daily" checked> Daily
    <br><br>
    <input type="radio" name="frequency" value="weekly"> Weekly

    Day:&nbsp<select name="day_of_week">
        <option value="1">Mon.</option>
        <option value="2">Tues.</option>
        <option value="3">Wed.</option>
        <option value="4">Thur.</option>
        <option value="5">Fri.</option>
        <option value="6">Sat.</option>
        <option value="0">Sun.</option>
    </select>          
    <br>
    <br>
    <input type="submit" name="execute" value="execute">
    """

    print """
    </form>
    </body>
    </html>
    """

        

    

    

    

    

