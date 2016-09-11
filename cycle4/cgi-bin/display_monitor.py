#!/usr/bin/env python
#Filename: display_monitor.py
#Written for Python 2.7
#IDEA:
#
#Student last logon by Prof. Thomas Havlversion of DSU
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 09/08/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#   This script will display the monstu database
#   
#   It is called by the POST method from monitor_student.html
#
#PARAMETERS FROM MONITOR_STUDENT.HTML:
#   f_class         class pattern
#   f_starting      starting from student
#   f_ending        ending with student
#   f_month         from month
#   f_day           from day
#   f_year          from year
#
#ALGORITHM:
#   Connect to the SQLITE db
#   Get the fields from the POST method
#   Select the rows from the db based upon the fields
#   Display the rows selected in html

#Modules
import cgi, cgitb 
import sqlite3
import subprocess
import socket
import datetime

#show any errors to the browser
cgitb.enable()

#determine if an editor found in the activity
def editor_found(activity) :
    #construct list of popular editors
    editors = ['vi', 'vim', 'gedit', 'nano', 'emacs', 'kate', 'kwrite', 'lime', 'pico', 'jed', 'geany', 'leaf', 'bluefish']

    #return true if editor found in activity
    for editor in editors :
        if editor in activity :
            return True

    #no editors in activity
    return False

now = datetime.datetime.now()

#Create instance of FieldStorage 
form = cgi.FieldStorage() 

#Get data from fields
pattern = str(form.getvalue('f_class'))
starting  = int(form.getvalue('f_starting'))
ending  = int(form.getvalue('f_ending'))
month  = int(form.getvalue('f_month'))
day  = int(form.getvalue('f_day'))
year = int(form.getvalue('f_year'))

#flip flop if necessary
if starting > ending :
    tmp = ending
    ending = starting
    starting = tmp

#student range
from_stud = str(pattern + "%02d" % starting)
to_stud = str(pattern + "%02d" % ending)   

#sqlite connection
sqlite_file = '/home/frankc/cycle4/monstu'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

#construct and execute sql select statement
sql_command = "SELECT * FROM student WHERE user BETWEEN '%s' AND '%s' AND month >= %d AND day >= %d and year >= %d" % (from_stud,to_stud,month,day,year) 
c.execute(sql_command)

#display results to html page

print "Content-type:text/html\r\n\r\n"
print """
<html>
<h1>DISPLAY EDITOR MONITOR RESULTS</h1>

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
print "Starting student: %s&nbsp;&nbsp;&nbsp;Ending Student: %s &nbsp;&nbsp;&nbsp;From Date: %02d / %02d / %02d <br>" % (from_stud,to_stud,month,day,year)
print "<br>"

#print the table Header
print "<table>"
print "<tr>"
print "<th>USER</th>"
print "<th>TTY</th>"
print "<th>FROM</th>"
print "<th>LOGIN@</th>"
print "<th>IDLE</th>"
print "<th>JCPU</th>"
print "<th>PCPU</th>"
print "<th>WHAT</th>"
print "</tr>"

#get the result set
all_rows = c.fetchall()

#go thru each row
for row in all_rows :
    
    #if there is an editor in the activity
    if editor_found(row[7]) :
        
        print "<tr>"

        #go thru and add the field into the table
        for i in range(0,8) :
            cell = "<td>" + row[i] + "</td>" 
            print cell

        print "</tr>"
    
print "</body>"
print "</html>"


