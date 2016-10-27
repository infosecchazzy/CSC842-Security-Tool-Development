#!/usr/bin/env python 
#Filename: schedule_last_logon.py
#Written for Python 2.7
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/01/2016
#Email: charles.frank@trojans.dsu.edu
#
import subprocess
import datetime
import time
import cgi, cgitb
import maintain_cron
import read_ini

# Schedule the last logon report
# Get the parameters from the last logon search screen
def schedule_last_logon_report() :
    
    #Create instance of FieldStorage 
    form = cgi.FieldStorage()

    #Get data from fields
    pattern = str(form.getvalue('f_class'))
    starting  = form.getvalue('f_starting')
    ending  = form.getvalue('f_ending')
    hour  = int(form.getvalue('f_hour'))
    minutes  = int(form.getvalue('f_minutes'))
    freq  = form.getvalue('frequency')
    dow  = int(form.getvalue('day_of_week'))

    s_date = str(form.getvalue('s_date'))
    t_date = str(form.getvalue('t_date'))

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

    #flip flop if necessary
    if starting > ending :
        tmp = ending
        ending = starting
        starting = tmp

    #start building the command
    cgi_home = read_ini.read_ini_parameter("LastLogon")['cgihome']
    e_l_l = read_ini.read_ini_parameter("LastLogon")['email_last_logon']
    
    ll_rpt = cgi_home + e_l_l
    ll_rpt = ll_rpt + " -p " + pattern
    ll_rpt = ll_rpt + " -s " + str(starting)
    ll_rpt = ll_rpt + " -e " + str(ending)
 

    #determine additional flags
    if l_flag :
        ll_rpt = ll_rpt + " -l" 
    if n_flag :
        ll_rpt = ll_rpt + " -n"
    if t_flag :
        ll_rpt = ll_rpt + " -t"

    #assign the dates
    ll_rpt = ll_rpt + " -y " + str(s_date)
    ll_rpt = ll_rpt + " -z " + str(t_date)

    ll_comment = read_ini.read_ini_parameter("LastLogon")['comment']

    #schedule report
    maintain_cron.schedule_report(ll_rpt,ll_comment,hour,minutes,freq,dow)

    #print the message that the report was scheduled
    print """
    <html>
    <body>
    <h1>Last Logon Report Scheduled</h1> 
    </body>
    </html>
    """
       
# schedule the last logon report to be emailed
if __name__ == "__main__" :
    schedule_last_logon_report()

   

        

    

    

    

    

