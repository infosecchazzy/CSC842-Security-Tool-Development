#!/usr/bin/env python
#Filename: lastlogon_chart.py
#Written for Python 2.7
#
#AUTHOR:
#    
#Charles V. Frank Jr.
#Date: 11/04/2016
#Email: charles.frank@trojans.dsu.edu
#
#USAGE: 
#usage: lastlogon_chart.py [-h] [-l] [-n] [-t] [-d <[x:y, x:y, .....]>]
#

from bokeh.charts import Bar, Scatter, output_file, show
import pandas as pd
import numpy as np
import shutil
import sys

import read_ini

#returns list separated by comma
def csv_list(string):
   return string.split(',')

#cleans up a line from the command line
def cleanse_line(alist) :

   a_line = str(alist)

   #get rid of single characters
   a_line = a_line.replace("[", "")
   a_line = a_line.replace("]", "")
   a_line = a_line.replace("'", "")
   a_line = a_line.replace(" ", "")

   #get rid of blank values
   a_line = a_line.replace(",,", ",")
   
   return a_line

#
# Build a data frame
#
def build_df(data_list, field1, field2) :

   #initialization
   studids = []
   y_vals = []
   raw_data = {}
   
   #split the list
   stud_yval = data_list.split(",")

   #go thru each record and build the field values
   for one_stud_yval in stud_yval :

      #split the record
      fields = one_stud_yval.split(":")

      #assign field values
      studids.append(str(fields[0]))

      if field2 == 'date' :
          date_text = str(fields[1])
          y = datetime.strptime(date_text, '%b-%d-%Y')
          y_vals.append(date_text)
      else:
          y_vals.append(int(fields[1]))

   #assign to raw_data
   raw_data[str(field1)] = studids
   raw_data[str(field2)] = y_vals

   #build the data frame
   df = pd.DataFrame(raw_data)
   
   return df

#
# Return the report file name
#
def get_rpt_name(target) :
    cgi_home = read_ini.read_ini_parameter("LastLogon")['tmpdir']
    chart_file = read_ini.read_ini_parameter("Charts")[target]
    chart_file = cgi_home + chart_file
    return chart_file
      
#
# Produce the last logon chart
#
def last_logon_chart(data_list) :

   #build the dataframe
   df = build_df(data_list, 'student', 'date')
   
   #make a scatter chart
   p = Scatter(df, yscale='datetime', x='student', y='date',
               marker='student', color='student',
               title="Last Logon Date Per Student",
               xlabel="Student Id",
               ylabel="Date")

   #output file
   html_file = get_rpt_name("lastlogin")
   output_file(html_file)
   
   #show the chart in a new browser
   show(p)

#
# Produce the num logon chart
#
def num_logon_chart(data_list) :

   #build the dataframe
   df = build_df(data_list, 'student', 'num_logons')

   #make a bar chart
   p = Bar(df, 'student', values='num_logons', color='student', title="Number of Logons Per Student")

   #output file
   html_file = get_rpt_name("numlogins")
   output_file(html_file)
   
   #show the chart in a new browser
   show(p)

#
# Produce the total logon chart
#
def tot_logon_chart(data_list) :

   #build the dataframe
   df = build_df(data_list, 'student', 'total_time')
   
   #donut time
   d = Donut(df, label=['student', 'total_time'], values='total_time',
             text_font_size='12pt', hover_text='total_time',
             title="Total Amount of Time (minutes) Per Student")

   #output file
   html_file = get_rpt_name("totaltime")
   output_file(html_file)
   
   #show the chart in a new browser
   show(d)
   
#
#Main routine:
#
#    import necessary modules
#
#    parse out the command line arguments
#

if __name__ == "__main__":
    import argparse
    import subprocess
    from datetime import datetime
    import time
    import socket
    import os
    from bokeh.charts import Bar, Scatter, Donut, output_file, show
    from bokeh.plotting import *
    import pandas as pd
    import numpy as np
    import shutil
    import sys
    import read_ini
    

    # Parse out the various options provided

    parser = argparse.ArgumentParser(description="DSU Linux User Last Logon Script Charts")

    parser.add_argument("-d",
                        nargs='+',
                        dest="data_list",
                        help="Data to include in the chart",
                        metavar="<PATTERN>")
    parser.add_argument("-l",
			action='store_true',
                        help="Last Logon of student Chart")
    parser.add_argument("-n",
			action='store_true',
                        help="Total Number of Logons Charts")
    parser.add_argument("-t",
			action='store_true',
                        help="Total Amount of Logon Time Chart")

    #get the arguments
    args = parser.parse_args()

    #cleanse the command line

    data_list = cleanse_line(args.data_list)

    print "Cleansed List: " + data_list
 
    
    #If the command line option was chosen
    #for the last logon information
    if (args.l) :
        last_logon_chart(data_list)


    #number of logons
    elif (args.n) :
        num_logon_chart(data_list)
        

    #total amount of time
    elif (args.t) :
        tot_logon_chart(data_list)

 
        

        


  
        

        

    

    

    

    

