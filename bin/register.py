#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from os import path
import calendar

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

base = path.realpath(path.join(path.dirname(__file__), '..'))
cmd = [ 'ledger'
      , 'register'
       ]

nargs = len(sys.argv[1:])
if nargs == 0:
    start = end = [None, None]
elif nargs == 1:
    start = end = reporting.parse(sys.argv[1])
else:
    start, end = map(reporting.parse, sys.argv[1:3])
    cmd += sys.argv[3:]

for datfile in reporting.list_datfiles(start, end):
    cmd.append('-f {}'.format(datfile))

print()
print("REGISTER".center(80))
if start == end:
    print("for {}, {}".format(calendar.month_name[int(end[1])], end[0]).center(80))
elif start[0] == end[0]:
    print("for {} through {}, {}".format( calendar.month_name[int(start[1])]
                                        , calendar.month_name[int(end[1])]
                                        , end[0]).center(80)
                                         )
else:
    print("for {}, {} through {}, {}".format( calendar.month_name[int(start[1])]
                                            , start[0]
                                            , calendar.month_name[int(end[1])]
                                            , end[0]
                                             ).center(80))
print()
print("Month     Payee                 Account                      Amount      Balance")
os.system(' '.join(cmd))
