#!/usr/bin/env python 
#Filename: student_monitoring_driver.py
#Written for Python 2.7
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 09/28/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#
#   This script will determine what action to perform based upon
#   the submit button pressed from student_monitoring.py
#

import cgi, cgitb
import last_stud
import mon_stud
import maintain_jobs

#show any errors to the browser
cgitb.enable()

#Create instance of FieldStorage 
form = cgi.FieldStorage()

#determine what to do based upon the submit button
if form.getvalue('lastlogon') :
    last_stud.last_stud_search()
elif form.getvalue('activitymon') :
    mon_stud.mon_stud_search()
elif form.getvalue('jobschedule') :
    maintain_jobs.maintain_reports()
elif form.getvalue('emails') :
    print "Under Construction"




    



        

    

    

    

    

