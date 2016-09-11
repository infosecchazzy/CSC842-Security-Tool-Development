STUDENT:

Charles V. Frank Jr.

DATE:

09/11/16

DESCRIPTION:

Cycle4 contains enhancements made from cycle1.  Now, the last logon and student monitoring utilites contain PYTHON CGI (Common Gateway Interface) to dynamically generate html web pages.  A daemon records the monitoring student activity wich is stored in a SQLITE database.

USAGE:

  Last Logon: http://your cgi bin location/last_stud.py

  Student Monitoring: http://your cgi bin location/mon_stud.py

PREREQS:

Since this tool is under construction, you will need to edit the PYTHON scripts to change the hard coded value of my home directory '/home/frankc/cycle4'.  Maybe, for another cycle, I will include each component of the tool in a standard LINUX location.

You will need PYTHON installed

You will need a CGI enabled web server.  For development, I simply ran PYTHONS http web server, python -m CGIHTTPServer, in my '/home/frankc/cycle4' directory.  I did not have any other web server running.

You will need SQLITE installed

DIRECTORY STRUCTURE:

cgi-bin - contains all of the python CGI scipts

daemon - conatins monitor_students.py for recording the student activity into the SQLITE db

sqlite - contains monstu SQLITE db that stores the student activity from monitor_students.py

