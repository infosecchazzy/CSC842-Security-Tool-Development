#!/usr/bin/env python 
# FileName: read_ini.py
# Student: Charles V. Frank Jr.
# Written for Python 2.7
#
# This file contains functionality to read the ini file
#
# https://wiki.python.org/moin/ConfigParserExamples

import ConfigParser

def read_ini_parameter(section) :

    #read the ini file
    Config = ConfigParser.ConfigParser()
    Config.read("/opt/studmon/studmon.ini")

    #return value(s) in a section
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
