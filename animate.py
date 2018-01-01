#!/usr/bin/env python3
# -*-encoding: utf-8-*-
import json
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import requests

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
        omni.context = 'watch : excellent animation'

        # do not output animates without complete defer time and those already in OmniFocus
        if len(item['defer']) < 12 or 'out' in item:
            # raise ValueError('defer time format error:{}'.format(item))
            continue
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
            child_omni.context = 'excellent animation'
            omni.append(child_omni)
    print(root)
    return root


def update_animate():
    """
    update bangumi release time from bilibili.com
    :return:
    """

    # get all bangumi raw time data
    js = get_raw_time_bangumis()
    result = []

    # extract release time from raw data
    for response in js:
        data = response['result']  # type: dir
        release_time = data['pub_time']  # type: str
        if release_time.endswith('00:00:01'):
            continue
        release_time = datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
        release_time = release_time.strftime('%Y%m%d%H%M')
        name = data['bangumi_title']
        result.append({'name': name, 'defer': release_time, 'bangumi_id': data['season_id']})
    print(result)

    # compare to storage file and update release time
    with open('animate2.json', 'r', encoding = 'utf-8') as f:
        raw = f.read()
    data = json.loads(raw)
    for item in result:
        for bangumi in data:
            if 'bilibili_bangumi_id' in bangumi and item['bangumi_id'] == bangumi['bilibili_bangumi_id']:
                bangumi['defer'] = item['defer']
    with open('animate2.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(data, ensure_ascii = False))


def get_no_list():
    """
    get bangumi id used in bilibili.com from the file
    :return:
    """
    with open('animate2.json', 'r', encoding = 'utf-8') as f:
        raw = f.read()
    js = json.loads(raw)
    res = []
    for item in js:
        note = item['note']  # type: str
        name = item['name']  # type: str
        if not note.startswith('https://bangumi.bilibili.com/anime/'):
            continue
        no = note[len('https://bangumi.bilibili.com/anime/'):-1]
        res.append(no)
        item['bilibili_bangumi_id'] = no

    with open('animate2.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(js, ensure_ascii = False))
    return res


def get_raw_time_bangumis():
    """
    get formatted data list contains release time.
    :return:
    """
    pool = ThreadPoolExecutor(20)
    future_list = []

    datas = get_no_list()
    for data in datas:
        future = pool.submit(request, data)
        future_list.append(future)
    res = []
    while len(future_list) > 0:
        for future in future_list:
            assert isinstance(future, Future)
            if future.done():
                data = process_data(future.result())
                res.append(data)
                future_list.remove(future)
    return res


def process_data(jsonp):
    """
    convert a single jsonp into a dict, head and foot should be defined
    :type jsonp: str
    """
    head = 'seasonListCallback('
    foot = ');'
    jsonp.strip()
    js = jsonp[len(head): -len(foot)]
    try:
        res = json.loads(js)
    except Exception as e:
        raise ValueError('jsonp convert error, raw data: {}]'.format(jsonp)) from e
    return res


def request(no):
    """
    request bangumi release raw data, aka jsonp.
    :type no: list[str]
    :param no: the list of bangumi id in str
    :return: jsonp string
    """
    useragent = 'ozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                'Chrome/63.0.3239.108 Safari/537.36 '
    url = 'https://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver?callback=seasonListCallback&jsonp=jsonp'.format(no)
    response = requests.get(url, headers = {'user-agent': useragent})
    return response.content.decode('utf-8')


def reset_animate_defer_date(animate_root, date):
    """
    :param animate_root: the root of animate.
    :param date: is datetime or date string 'yyyymmddhhmm'
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
    update_animate()
    generate_animate()
