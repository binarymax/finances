#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from os import path
import calendar

ourdir = path.realpath(path.dirname(__file__))
sys.path.insert(0, ourdir)

import reporting

base = path.realpath(path.join(path.dirname(__file__), '..'))
cmd = [ 'ledger'
      , 'balance'
      , '^Income'
      , '^Expense'
      , '--prepend-width=0' # this is here to satisfy ledger on Travis
      , '--limit "not (payee =~ /^Retained Earnings$/)"'
      , '--sort "account =~ /^Income.*/ ? 0 : '
      ,        '(account =~ /^Expense.*/ ? 1 : 2))"'
       ]
cmd += sys.argv[1:]

start, end = reporting.parse(sys.argv[1:])
cmd += reporting.list_datfiles(start, end)

print()
print("INCOME STATEMENT".center(42))
if start == end:
    print("for {}, {}".format(calendar.month_name[int(end[1])], end[0]).center(42))
elif start[0] == end[0]:
    print("for {} through {}, {}".format( calendar.month_name[int(start[1])]
                                        , calendar.month_name[int(end[1])]
                                        , end[0]).center(42)
                                         )
else:
    print("for {}, {} through {}, {}".format( calendar.month_name[int(start[1])]
                                            , start[0]
                                            , calendar.month_name[int(end[1])]
                                            , end[0]
                                             ).center(42))
print()
reporting.report(cmd)
