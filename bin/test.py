#!/usr/bin/env python2.7 -u
from __future__ import absolute_import, division, print_function, unicode_literals

import commands
import sys
import traceback
from os import path
from decimal import Decimal as D


root = path.realpath(path.dirname(__file__))
report_script = lambda a: a.replace(' ', '-') + '.py'


def report(name, just_accounts=False):
    status, report = commands.getstatusoutput(report_script(name) + ' --flat')
    if status > 0:
        raise SystemExit(report)
    for line in report.splitlines():
        if just_accounts:
            if line.startswith('------------') or not line: break
            yield line.split(None, 2)
        else:
            yield line.strip()


def accounts(name):
    return report(name, just_accounts=True)


def account(report, account):
    total = D(0)
    for currency, amount, account in accounts('balance sheet'):
        if account == 'Equity:Current Activity':
            total += D(amount)
    return total


def total(name):
    total = D(0)
    for line in report(name):
        if line.startswith('$'):
            try:
                currency, total, _ = line.split(None, 2)
            except ValueError:
                currency, total = line.split()
                break
    return D(total)


def test_escrow_balances():
    escrow_assets = escrow_liability = D(0)

    for currency, amount, account in accounts('balance sheet'):
        if account.startswith('Assets:Escrow:'):
            escrow_assets += D(amount)
        if account.startswith('Liabilities:Escrow'):
            escrow_liability += D(amount)

    print(escrow_assets, escrow_liability)
    assert escrow_assets + escrow_liability == 0


def test_income_balances():
    for currency, amount, account in accounts('balance sheet'):
        assert not account.startswith('Income:')
    print('good')


def test_expenses_balance():
    for currency, amount, account in accounts('balance sheet'):
        assert not account.startswith('Expenses:')
    print('good')


def test_fee_buffer_reconciles():

    fee_income = fee_expense = fee_buffer = D(0)

    for currency, amount, account in accounts('balance sheet'):
        if account.startswith('Assets:Fee Buffer:'):
            fee_buffer += D(amount)

    for currency, amount, account in accounts('fee buffer statement'):
        if account.startswith('Income:Fee Buffer:'):
            fee_income -= D(amount)
        if account.startswith('Expenses:Fee Buffer:'):
            fee_expense -= D(amount)

    delta = fee_income + fee_expense
    print(fee_income, fee_expense, delta, fee_buffer, abs(delta-fee_buffer))
    assert delta == fee_buffer


def test_net_income_reconciles_with_current_activity():
    net_income = total('income statement')
    current_activity = account('balance sheet', 'Equity:Current Activity')
    print(net_income, current_activity)
    assert net_income == current_activity


if __name__ == '__main__':
    nfailures = 0
    filt = sys.argv[1] if len(sys.argv) > 1 else ''
    for name, test_func in globals().items():
        if name.startswith('test_') and filt in name:
            print(name, "... ", end='')
            try:
                test_func()
            except:
                nfailures += 1
                traceback.print_exc()
                print()
    raise SystemExit(nfailures)
