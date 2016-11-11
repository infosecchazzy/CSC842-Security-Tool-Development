#!/usr/bin/env python
#Filename: email_existing_llog.py
#Written for Python 2.7
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/1/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESC: The exisitng last logon report is emailed

#
#Main routine:
#
#    import necessary modules
#

import cgi, cgitb
import email_last_logon
import email_rpt

def lastlogon_rpt() :

    #set the standard out to a file name
    filename = email_last_logon.generate_filename()

    #email the last logon report
    email_rpt.email_last_logon(filename)

    #display message
    print """
    <html>
    <body>
    <h1>Please check your email</h1>
    </body>
    </html>
    """
  
        

        

    

    

    

    

