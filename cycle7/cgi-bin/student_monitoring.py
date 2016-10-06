#!/usr/bin/env python
#Student: Charles V. Frank Jr.
#Email: charles.frank@trojans.dsu.edu
#Date: 09/28/2016
#File: student_monitoring.py
#Desc: 
#	Main page for student monitoring 	
#
#
import cgi, cgitb 
print """
<html>
<body>
<form action="/cgi-bin/student_monitoring_driver.py" method="post">
<h1>STUDENT MONITORING</h1>
<input type="submit" name="lastlogon" style="width:200px; height:80px" value="Last Logon" />
<br>
<br>
<input type="submit" name="activitymon" style="width:200px; height:80px" value="Activity Monitoring" />
<br>
<br>
<input type="submit" name="jobschedule" style="width:200px; height:80px" value="Job Scheduling" />
<br>
<br>
<input type="submit" name="emails" style="width:200px; height:80px" value="Email Addresses" />
</form>
</body>
</html>
"""
