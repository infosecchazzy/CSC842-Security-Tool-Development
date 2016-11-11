#!/usr/bin/env python 
#Filename: last_logon_driver.py
#Written for Python 2.7
#IDEA:
#
#This script was requested by Prof. Thomas Havlversion of DSU
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 09/28/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#
#   This script will determine whether to show the last logon
#   report to the web browser or schedule the search in cron.
#
#   Called by last_stud.py
#    
#POST PARAMETERS:
#
#   f_class         Class
#   f_starting      Starting with student
#   f_ending        Ending with Student
#   last_report     Last Logon report requested
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
import cgi, cgitb
import last_logon
import email_last_logon
import sys

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
#student data
pattern = str(form.getvalue('f_class'))
starting  = int(str(form.getvalue('f_starting')))
ending  = int(str(form.getvalue('f_ending')))

#since to date
s_date  = str(form.getvalue('since_date'))

#ending date
e_date = str(form.getvalue('ending_date'))

#calculate the since date
#s_date = "%04d%02d%02d" % (f_year, f_month, f_day)

#calculate the to date
#t_date = "%04d%02d%02d" % (t_year, t_month, t_day)

#swap if necessary
#if int(s_date) > int(t_date) :
#    tmp_date = t_date
#    t_date = s_date
#    s_date = tmp_date
    
#append the time at the end
#s_date = s_date + "000000"             
#t_date = t_date + "235959"

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

if form.getvalue('search') :
    search_flag = True
else :
    search_flag = False

if form.getvalue('schedule') :
    schedule_flag = True
else :
    schedule_flag = False

#flip flop if necessary
if starting > ending :
    tmp = ending
    ending = starting
    starting = tmp

#determine what button was pressed
#search button pressed
if search_flag : 

    #get student list
    student_list = []
    student_list = last_logon.get_student_list(pattern, starting, ending)

    #call display logon with parameters
    
    #set the standard output to a file name
    file_name = email_last_logon.generate_filename()
    last_logon.display_last_logon(student_list,
                                  l_flag,
                                  n_flag,
                                  t_flag,
                                  s_date,
                                  e_date,
                                  file_name)

    #show the report in the browser
    last_logon.display_last_logon(student_list,
                                  l_flag,
                                  n_flag,
                                  t_flag,
                                  s_date,
                                  e_date,
                                  "")

#schedule button pressed
elif schedule_flag :

    #call the schedule form
    last_logon.schedule_last_logon(pattern,
                                   starting,
                                   ending,
                                   l_flag,
                                   n_flag,
                                   t_flag,
                                   s_date,
                                   e_date)
    



        

    

    

    

    

