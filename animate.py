#!/usr/bin/env python3
# -*-encoding: utf-8-*-
import json
from datetime import timedelta

from omni import *


def defer_one_week(root):
    """
    :type root: Omni
    """
    one_week = timedelta(weeks = 1)
    if not root.defer == '':
        defer = root.defer_time('datetime')
        defer += one_week
        root.defer_time(defer)
    for omni in root:
        defer_one_week(omni)


def generate_animate():
    with open('animate.json', 'r', encoding = 'utf-8') as f:
        raw = json.loads(f.read())
    root = Omni()
    for item in raw:
        if item['note'] == '':
            continue
        omni = Omni()
        omni.name = item['name']
        omni.parallel = True
        omni.auto_done = True
        omni.note = item['note']
        if len(item['defer']) < 12:
            raise ValueError('defer time format error:{}'.format(item))
        try:
            start_time = datetime.strptime(item['defer'], serial_format)
        except ValueError as e:
            raise ValueError('defer time format error:{}'.format(item))
        week = timedelta(weeks = 1)
        root.append(omni)
        if item['e'] == '':
            item['e'] = '12'
        for i in range(int(item['e'])):
            child_omni = Omni()
            child_omni.name = omni.name + ' - ' + str(i + 1)
            child_omni.note = omni.note
            child_omni.defer = start_time + week * i
            omni.append(child_omni)
    print(root)


def reset_animate_defer_date(animate_root, date):
    """
    animate_root is the root of animate.
    date is datetime or date string 'yyyymmddhhmm'
    :type animate_root: Omni
    """
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, serial_format)
        except ValueError as e:
            raise ValueError('date: [{}] format error.'.format(date)) from e
    elif isinstance(date, datetime):
        pass
    else:
        raise TypeError('date should be datetime or date string "yyyymmddhhmm"')

    one_week = timedelta(weeks = 1)

    for item in animate_root:
        item.defer_time(date)
        date += one_week
    return animate_root

if __name__ == '__main__':
    omni = Omni.read(path = '/Users/GeniusV/Desktop/omni')
    for item in omni:
        reset_animate_defer_date(item, '201801010000')
    print(omni)