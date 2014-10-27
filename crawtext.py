#!/usr/bin/env python
# -*- coding: utf-8 -*-

__name__ = "crawtext"
__version__ = "3.1.0b1"
__doc__ = '''Crawtext.
Description:
A simple crawler in command line.

Usage:
	crawtext.py (<name>|<user>|<url>)
	crawtext.py <url> 
	crawtext.py <name> <action> [--repeat=<repeat>] [--format=<format>] [--data=<data>] [--file=<input>] [--url=<input>] [--out=<outputfile>]
	crawtext.py <name> [--user=<email>] [--query=<query>] [--key=<key>] [--repeat=<repeat>] [ --format=<format> ]
	crawtext.py (-h | --help)
	crawtext.py --version

Help:
crawtext.py <name> report --format=(txt|html|pdf|mail)
crawtext.py <name> export --format=(csv|json)
crawtext.py <name> schedule --repeat=<repeat>
crawtext.py <name> unschedule [--task=<task>]
crawtext.py <name> report [--format=<format>]
crawtext.py <name> export [--format= --coll_type=<coll_type>]
crawtext.py <name> debug
crawtext.py <name> list
crawtext.py <name> -s add (<url>|<file>)
crawtext.py <name> -s expand
crawtext.py <name> -s delete [<url>]

'''



from docopt import docopt
from worker.worker import Worker
import os, sys

ABSPATH = os.path.dirname(os.path.abspath(sys.argv[0]))

if __name__== "crawtext":
	try:		
		w = Worker(docopt(__doc__), debug=True)		
	except KeyboardInterrupt:
		sys.exit()
