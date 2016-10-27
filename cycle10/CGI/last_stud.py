#!/usr/bin/env python
#Student: Charles V. Frank Jr.
#Email: charles.frank@trojans.dsu.edu
#Date: 09/07/2016
#File: last_stud.py
#Desc: Web page to allow for search selection for student last logon
#	Calls display_last_logon.py to search for last logon info
#
#
import cgi, cgitb
import time
cgitb.enable()

def last_stud_search() :
    #calculate month/day/year for defaults
    curr_day = time.strftime("%d")
    curr_month = time.strftime("%m")
    curr_year = time.strftime("%y")

    prev_month = int(curr_month) - 1
    if prev_month < 1 :
        prev_month = 12

    #generate the html for the date fields
    prev_month_html = 'Month: <input type="number" name="f_month" min="1" max="12" value="'+ str(prev_month) + '" required>'    
    prev_day_html = 'Day: <input type="number" name="f_day" min="1" max="32" value="' + "1" + '" required>'
    prev_year_html = 'Year: <input type="number" name="f_year" min="0" max="99" value="' + curr_year + '" required>'
 
    curr_month_html = 'Month: <input type="number" name="t_month" min="1" max="12" value="'+ curr_month + '" required>'
    curr_day_html = 'Day: <input type="number" name="t_day" min="1" max="32" value="' + curr_day + '" required>'
    curr_year_html = 'Year: <input type="number" name="t_year" min="0" max="99" value="' + curr_year + '" required>'

    print """
    <html>
    <body>
    <form action="/cgi-bin/last_logon_driver.py" method="post">
    <h1>STUDENT LAST LOGON MONITORING</h1>
    """
    print """
    <p>Student Range</p>
    Class: <input type="text" name="f_class" required maxlength = "6"><br><br>
    Starting Student: <input type="number" name="f_starting" min=0 max=99 value="0" required><br><br>
    Ending Student: <input type="number" name="f_ending" min=0 max=99 value="1" required><br><br>
    <p>Since Date</p>
    """
    print prev_month_html
    print prev_day_html
    print prev_year_html

    print """
    <p>To Date</p>
    """

    print curr_month_html
    print curr_day_html
    print curr_year_html

    print "<br><br>"
    
    print """
    <p>Reporting Level</p>
    <input type="checkbox" name="last_report" value="on" checked /> Last Report
    <input type="checkbox" name="num_logins" value="on" checked /> Num Logins
    <input type="checkbox" name="total_time" value="on" checked /> Total Time
    <br><br>
    <input type="submit" name="search" value="search">
    <input type="submit" name="schedule" value="schedule">
    </form>
    </body>
    </html>
    """
