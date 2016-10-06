#!/usr/bin/env python 
#Filename: maintain_cron.py
#Written for Python 2.7
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/02/2016
#Email: charles.frank@trojans.dsu.edu
#
import subprocess
import datetime
import time
from crontab import CronTab

#return all the jobs in cron
def list_scheduled_reports() :
   
    #empty list of scheduled reports
    scheduled_jobs = []

    #cron user
    cronu = "frankc"

    #assign the crontab
    cront = CronTab(user=cronu)

    #build the list of cron jobs
    for job in cront:
        scheduled_jobs.append(job)

    #return the list of jobs
    return scheduled_jobs

#
#delete a cron job
#
def delete_scheduled_report(target) :

    #cron user
    cronu = "frankc"

    #assign the crontab
    cront = CronTab(user=cronu)

    #find the job in cron
    for job in cront:

        #target found as a job
        if str(target) in str(job) :
        
            #remove job
            cront.remove(job)

            #write results to the cron
            cront.write()
  

#schedule a report in cron
#
#Parameters:
#   report - report to execute
#   rpt_comment - report comment to include in cron
#   hour - hour
#   minutes - minutes
#   freq - daily/weekly
#   day_of_week - day of week

def schedule_report(report, rpt_comment, hour, minutes, freq, day_of_week) :

    #cron user
    cronu = "frankc"

    #assign the crontab
    cront = CronTab(user=cronu)

    #make descriptive comment
    rpt_comment = rpt_comment + " - " + freq
    
    #create the new cron job
    cron_job = cront.new(command=report, comment=rpt_comment)

    #set the hour/minutes for the job
    cron_job.minute.on(minutes)
    cron_job.hour.on(hour)

    #weekly frequency for the cron job
    if "weekly" in freq.lower() :
        cron_job.dow.on(day_of_week)

    #enable the cron job
    cron_job.enable()

    #write out the crontab with the new job
    cront.write()


   

        

    

    

    

    

