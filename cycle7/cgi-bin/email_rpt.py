#!/usr/bin/env python
#Filename: email_rpt.py
#Written for Python 2.7
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 10/91/2016
#Email: charles.frank@trojans.dsu.edu
#
#DESC: contains routines to email a report

import cgi, cgitb
import subprocess
import datetime
import time
import socket
import smtplib
import email.utils
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys

#send an email
#Adapted from python docs
def send_mail(send_from, send_to, subject, text, filename) :

    #setup the header
    outer = MIMEMultipart()
    outer['Subject'] = subject
    me = send_from
    family = send_to
    outer['From'] = me
    outer['To'] = family

    #set global variable
    path = filename

    # Guess the content type based on the file's extension.  Encoding
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(path) as fp:
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(path, 'rb') as fp:
            msg = MIMEImage(fp.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(path, 'rb') as fp:
            msg = MIMEAudio(fp.read(), _subtype=subtype)
    else:
        with open(path, 'rb') as fp:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
        # Encode the payload using Base64
        encoders.encode_base64(msg)
        
    # Set the filename parameter
    filename= str(os.path.basename(path))
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    outer.attach(msg)
    
    # Now send the message
    composed = outer.as_string()

    #send the email
    s = smtplib.SMTP('localhost')
    s.sendmail(send_from, send_to, composed)
    

#email last logon report
def email_last_logon(filename) :

    #set some email parameters
    send_from = "monitor_students"
    send_to = "infosec_chazzy@yahoo.com"
    subject = "Last Logon Report"
    text = "Last Logon Report attached"

    #send the email
    send_mail(send_from, send_to, subject, text, filename)
         

    

    



  
        

        

    

    

    

    

