#!/usr/bin/env python
#Filename: monitor_student.py
#Written for Python 2.7
#IDEA:
#
#Student last logon by Prof. Thomas Havlversion of DSU
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 08/25/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESCRIPTION:
#   This script will execute in an infinite loop and store the
#   output of the w command into a sqlite database
#
#Python Daemon Reference: http://stackoverflow.com/questions/473620/
#                                how-do-you-create-a-daemon-in-python
#
#

#Modules

import sqlite3
import subprocess
import socket
import datetime
import time

#return the month number

def month_num(name):
    if name == "Jan" : return 1
    elif name == "Feb" : return 2
    elif name == "Mar" : return 3
    elif name == "Apr" : return 4  
    elif name == "May" : return 5
    elif name == "Jun" : return 6
    elif name == "Jul" : return 7
    elif name == "Aug" : return 8
    elif name == "Sep" : return 9
    elif name == "Oct" : return 10
    elif name == "Nov" : return 11
    elif name == "Dec" : return 12
    else: return 0


#initialization
#in the future, maybe these parameters could be read
#from an initialization file
   
#default paths
stdin_path = '/dev/null'
stdout_path = '/dev/tty'
stderr_path = '/dev/tty'
pidfile_path =  '/tmp/foo.pid'
pidfile_timeout = 5

#sqllite db
sqlite_file = '/home/frankc/cycle4/monstu'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
sql_command = "PRAGMA journal_mode = WAL"
c.execute(sql_command)
conn.commit()
sql_command = "PRAGMA synchronous = NORMAL"
c.execute(sql_command)
conn.commit()

#error file
err_file = '/home/frankc/monitor_student.err' 

#wait time
wait_time = 60

#execute the w command
#store results in monogdb
        
#construct linux command   
linux_cmd = "w -h " 

#infinite loop
while True:
    
    #open a process with the linux command 
    p = subprocess.Popen(linux_cmd, stdout=subprocess.PIPE, shell=True)

    #gather the output from the command
    (output, err) = p.communicate()

    #wait for the command to finish
    p_status = p.wait()

    #if an error occured
    if err is not None:
        with open(err_file, "a") as err_f:
                    err_f.write(err)
                    err_f.write('\n')
                    err_f.close()
               

    #split into lines
    lines = output.splitlines()

    #for each line of the w command
    #w header looks like:
    #USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    for a_line in lines :

        #split the line to get each field
        wf = a_line.split()

        #the what could contain spaces
        #what command
        wc =""
        pos = 0

        # go thru each field in the line
        for fields in wf :

            #if at the what column, build the what command
            if pos == 7 :
                wc = fields
            if pos > 7 :
                wc = wc + " " + fields

            #increment across the columns
            pos = pos + 1

        #convert login field wf[3] to DDMonthYY
        #could be in format: DDMonthYY or DayDD
        f_login = wf[3]
        now = datetime.datetime.now()
        f_year = now.strftime("%y")
        f_month = now.strftime("%B")
        f_month = f_month[:3]
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        #if the date is in format DaysDD
        if f_login[:3] in days :
            f_day = f_login[3:]
            f_login = f_day + f_month + f_year
        #if date is in format HH:MM
        if ":" in f_login :
            f_day = now.strftime("%d")
            f_login = f_day + f_month + f_year

        #cslculate numeric version of month, day, year
        #SQLite does not have a date field
        n_year = int(f_login[-2:])
        z = len(f_login)
        start_at = z - 5
        #print(f_login[ start_at : ( start_at + 3 )])
        n_month = int(month_num(f_login[ start_at : ( start_at + 3 )]))
        n_day = int(f_login[:( start_at )])    

        #delete a record if it already exists
        #ensures no duplicates
        sql_command = """DELETE FROM student WHERE user = '%s' and tty = '%s' and host = '%s' and login = '%s' and what = "%s" """ % (wf[0],wf[1],wf[2],wf[3],wc)
        print sql_command
        c.execute(sql_command)
        conn.commit()

        #insert the record
        sql_command = """INSERT INTO student(user, tty, host, login, idle, jcpu, pcpu, what, month, day, year) VALUES ('%s','%s','%s','%s','%s','%s','%s',"%s",%d,%d,%d)""" % (wf[0],wf[1],wf[2],wf[3],wf[4],wf[5],wf[6],wc,n_month,n_day,n_year)
        print sql_command
        c.execute(sql_command)
        conn.commit()

    #wait to do all over again
    time.sleep(wait_time)



