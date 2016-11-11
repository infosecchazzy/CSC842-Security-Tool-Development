#!/usr/bin/env python
#Student: Charles V. Frank Jr.
#Email: charles.frank@trojans.dsu.edu
#Date: 09/07/2016
#File: mon_stud.py
#Desc: Web page to allow for search selection for student monitoring
#	Calls display_monitor.py to search thru sqlite db
#
#
import cgi, cgitb

def mon_stud_search() :
    print """
    <html>
    <body>
    <form action="/cgi-bin/display_monitor.py" method="post">
    <h1>STUDENT EDITOR MONITORING</h1>
    <p>Student Range</p>
    Class: <input type="text" name="f_class" required maxlength = "6"><br><br>
    Starting Student: <input type="number" name="f_starting" min=0 max=99 value="0" required><br><br>
    Ending Student: <input type="number" name="f_ending" min=0 max=99 value="1" required><br><br>
    <p>From Date</p>
    Month: <input type="number" name="f_month" min="1" max="12" value="1" required>
    Day: <input type="number" name="f_day" min="1" max="32" value="1" required>
    Year: <input type="number" name="f_year" min="0" max="99" value="16" required><br><br>
    <input type="submit">
    </form>
    </body>
    </html>
    """
