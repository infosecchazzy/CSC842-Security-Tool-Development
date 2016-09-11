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
cgitb.enable()
print """
<html>
<body>
<form action="/cgi-bin/display_last.py" method="post">
<h1>STUDENT LAST LOGON MONITORING</h1>
<p>Student Range</p>
Class: <input type="text" name="f_class" required maxlength = "6"><br><br>
Starting Student: <input type="number" name="f_starting" min=0 max=99 value="0" required><br><br>
Ending Student: <input type="number" name="f_ending" min=0 max=99 value="1" required><br><br>
<p>Reporting Level</p>
<input type="checkbox" name="last_report" value="on" checked /> Last Report
<input type="checkbox" name="num_logins" value="on" checked /> Num Logins
<input type="checkbox" name="total_time" value="on" checked /> Total Time
<br><br>
<input type="submit">
</form>
</body>
</html>
"""
