#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 4/24/18.
from datetime import datetime, timedelta

from omnifocus.omni import Omni

tod = datetime(year = datetime.now().year, month = datetime.now().month, day = datetime.now().day)
d1 = timedelta(days = 1)
w1 = timedelta(weeks = 1)
h6 = timedelta(hours = 6)
h1 = timedelta(hourse = 1)
h2 = timedelta(hourse = 2)
h3 = timedelta(hourse = 3)
h4 = timedelta(hourse = 4)
h5 = timedelta(hourse = 5)
h6 = timedelta(hourse = 6)
h7 = timedelta(hourse = 7)
h8 = timedelta(hourse = 8)
h9 = timedelta(hourse = 9)
h10 = timedelta(hourse = 10)
h11 = timedelta(hourse = 11)
h12 = timedelta(hourse = 12)
h13 = timedelta(hourse = 13)
h14 = timedelta(hourse = 14)
h15 = timedelta(hourse = 15)
h16 = timedelta(hourse = 16)
h17 = timedelta(hourse = 17)
h18 = timedelta(hourse = 18)
h19 = timedelta(hourse = 19)
h20 = timedelta(hourse = 20)
h21 = timedelta(hourse = 21)
h22 = timedelta(hourse = 22)
h23 = timedelta(hourse = 23)

if __name__ == '__main__':
    root = Omni()
    for i in range(4):
        child = Omni()
        child.name = "review embed middle exam"
        child.defer = tod + d1 * i + h6
        child.due = tod + d1 * i + h23
        root.append(child)

    print(root)

