#!/usr/bin/env python
#Student: Charles V. Frank Jr.
#Email: charles.frank@trojans.dsu.edu
#Date: 10/05/2016
#File: maintain_jobs.py
#Desc: Web page to allow for maintaining jobs
import subprocess
import datetime
import time
import cgi, cgitb
import maintain_cron

#maintain scheduled reports
def maintain_reports() :
    #build the list of cronjobs
    cronjobs = []
    cronjobs = maintain_cron.list_scheduled_reports()

    print cronjobs

    #build the html page
    print """
    <html>
    <body>
    <form action="/cgi-bin/delete_jobs.py" method="post">
        <h1>MAINTAIN SCHEDULED REPORTS</h1>
    """
    print """
        <select name="job">
    """

    #add cronjobs to the list
    for cjob in cronjobs :
        print '<option value="' + str(cjob) + '">'
        print "%s" % str(cjob) + "</option>"
    
    print "</select>"          

    print """
        <br><br>
        <input type="submit" name="delete" value="delete">
        </form>
        </body>
        </html>
    """

#main

if __name__ == "__main__" :
    maintain_reports()
