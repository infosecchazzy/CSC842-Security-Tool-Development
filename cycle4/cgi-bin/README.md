STUDENT:

  Charles V. Frank Jr.
  
DATE:

  09/11/16

DESCRIPTION:

  This directory contains the Python CGI scripts to execute the last logon report and monitoring report
  
SCRIPTS:

  last_stud.py - last logon search criteria
  
  display_last.py - display last logon report based upon search criteria
  
  mon_stud.py - monitor student search criteria
  
  display_monitor.py - display monitor report
  
FLOW:

  last_stud.py   POST 
        display_last.py
        
  mon_stud.py   POST
        display_monitor.py
  
  
