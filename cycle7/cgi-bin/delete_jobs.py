#!/usr/bin/env python
#Student: Charles V. Frank Jr.
#Email: charles.frank@trojans.dsu.edu
#Date: 10/05/2016
#File: delete_jobs.py
#Desc: Delete a job
#Parameter: job from the previous from maintain_jobs.py
import subprocess
import datetime
import time
import cgi, cgitb
import maintain_cron

#show any errors to the browser
cgitb.enable()

#Create instance of FieldStorage 
form = cgi.FieldStorage()

#Get data from fields
target = str(form.getvalue('job'))

#delete the job
maintain_cron.delete_scheduled_report(target)

#build the html page
print """
<html>
<body>
    <form action="/cgi-bin/maintain_jobs.py" method="post">
    <h1>JOB DELETED .....</h1>
    <input type="submit" name="return" value="return">
"""

print """
     </form>
    </body>
    </html>
"""
