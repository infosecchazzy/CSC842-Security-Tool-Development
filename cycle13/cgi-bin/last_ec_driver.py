#!/usr/bin/env python 
#Filename: last_ec_driver.py
#Written for Python 2.7
#IDEA:
#
#This script was requested by Prof. Thomas Havlversion of DSU
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 11/05/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#
#   This script will determine whether to email or produce charts
#   from the last logon report
#
#   Called by last_logon.py
#    

import subprocess
import sys
import datetime
import time
import os
import cgi, cgitb
import email_existing_llog
import read_ini

#
# A browser tab will be generated with the python chart
#

def generate_chart( py_cmd ) :
  
    #run the python command
    os.system(py_cmd)
        

#
#Main routine:
#

#show any errors to the browser
cgitb.enable()

#Create instance of FieldStorage 
form = cgi.FieldStorage()

#determine the button pressed
#email button pressed
if form.getvalue('email') :
    email_existing_llog.lastlogon_rpt()

#charts button pressed
elif form.getvalue('charts') :

    #form the py command to execute the report
    cgi_home = read_ini.read_ini_parameter("LastLogon")['cgihome']
    chart_rpt = read_ini.read_ini_parameter("Charts")['chartrpt']
    chart_py = cgi_home + chart_rpt
    
    #Get data from fields

    lastlogons = str(form.getvalue('glastlog'))

    if "None" not in lastlogons :

        #construct py command
        py_cmd = chart_py + " -l" + " -d " + lastlogons

        #call py command to generate the chart
        generate_chart(py_cmd)

    #Get data from fields

    numlogons = str(form.getvalue('gnumlog'))

    if "None" not in numlogons :

        #construct py command
        py_cmd = chart_py + " -n" + " -d " + numlogons

        #call py command to generate the chart
        generate_chart(py_cmd)

    #Get data from fields

    totlogons = str(form.getvalue('gtotlog'))

    if "None" not in totlogons :
        
        #construct py command
        py_cmd = chart_py + " -t" + " -d " + totlogons

        #call py command to generate the chart
        generate_chart(py_cmd)
        
    #print the message that the charts were generated
    print """
    <html>
    <body>
    <h1>Charts Generated... </h1> 
    </body>
    </html>
    """


    



        

    

    

    

    

