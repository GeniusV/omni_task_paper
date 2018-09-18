#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 5/30/18.
import argparse
import json
import re
import sys
from datetime import datetime, timedelta

import requests
from omnifocus.omni import Omni

tod = datetime(year = datetime.now().year, month = datetime.now().month, day = datetime.now().day)

d1 = timedelta(days = 1)

w1 = timedelta(weeks = 1)

h1 = timedelta(hours = 1)
h2 = timedelta(hours = 2)
h3 = timedelta(hours = 3)
h4 = timedelta(hours = 4)
h5 = timedelta(hours = 5)
h6 = timedelta(hours = 6)
h7 = timedelta(hours = 7)
h8 = timedelta(hours = 8)
h9 = timedelta(hours = 9)
h10 = timedelta(hours = 10)
h11 = timedelta(hours = 11)
h12 = timedelta(hours = 12)
h13 = timedelta(hours = 13)
h14 = timedelta(hours = 14)
h15 = timedelta(hours = 15)
h16 = timedelta(hours = 16)
h17 = timedelta(hours = 17)
h18 = timedelta(hours = 18)
h19 = timedelta(hours = 19)
h20 = timedelta(hours = 20)
h21 = timedelta(hours = 21)
h22 = timedelta(hours = 22)
h23 = timedelta(hours = 23)

index_url = 'https://www.bilibili.com/anime/index/?spm_id_from=333.334.primary_menu.13#season_version=-1&area=2&is_finish=-1&copyright=-1&season_status=-1&season_month=10&pub_date=2018&style_id=-1&order=3&st=1&sort=0&page=1'
# index_url = 'https://www.bilibili.com/anime/index/?spm_id_from=333.334.primary_menu.13#season_version=-1&area=2&is_finish=-1&copyright=-1&season_status=-1&season_month=10&pub_date=2018&style_id=-1&order=3&st=1&sort=0&page=1'
INDEX_JSON_URL='https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=2&is_finish=0&copyright=-1&season_status=-1&season_month={season_month}&pub_date={pub_date}&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize=30'
BILIBILI_BANGUMI_DETAIL_URL = 'https://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver?callback=seasonListCallback&jsonp=jsonp'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/63.0.3239.108 Safari/537.36 '

serial_format = '%Y%m%d%H%M'
omni_format = '%Y-%m-%d %H:%M'

root = Omni()


def get_bangumi_count(id):
    json_data = get_json_data(BILIBILI_BANGUMI_DETAIL_URL.format(id),
                              head = 'seasonListCallback(',
                              foot = ');')
    result = json.loads(json_data)
    data = result['result']
    if 'total_count' in data:
        return int(data['total_count'])
    return 12


def get_json_data(url, head = '', foot = ''):
    """
    For jsonp usage example:
        json_data = get_json_data('http://example.com/web_api/', head =  'seasonListCallback(', foot =  ');')

    :param url:
    :param head: If you use this param and foot, this method will get into jsonp mode and return json string.
    :param foot: If you use this param and head, this method will get into jsonp mode and return json string.

    :rtype str
    :return: json string
    """
    raw_response = requests.get(url, headers = {"user-agent": USER_AGENT}).content.decode()
    if not head == '' and not foot == '':
        raw_response.strip()
        json_string = raw_response[len(head): -len(foot)]
        return json_string
    return raw_response


def generate(name, id, start: datetime, e, note = ''):
    if not note:
        note = ''
        if id:
            note = 'https://bangumi.bilibili.com/anime/{}'.format(id)

    # Param check
    if not name:
        print('Name is empty.')

    template = "{} - {}"
    context = 'watch : excellent animation'
    main = Omni()
    main.name = name
    main.context = context
    main.parallel = True

    if not e:
        e = 12
        if id:
            e = get_bangumi_count(id)

    for i in range(1, e + 1):
        defer = start + w1 * (i - 1)
        child = Omni()
        child.name = template.format(name, i)
        child.defer = defer
        child.context = context
        child.note = note
        main.append(child)
    root.append(main)


def get_defer(delay, defer):
    result = datetime.now()
    match = re.match('(\d)([WwdD])', delay)

    if len(root.child) > 0:
        result = datetime.strptime(root.child[0].defer, omni_format)

    if match:
        num = int(match.group(1))
        suffix = match.group(2)
        delta = timedelta()
        if suffix.lower() == 'w':
            delta = timedelta(weeks = num)
        if suffix.lower() == 'd':
            delta = timedelta(days = num)

        start = datetime.now()
        if len(root.child) > 0:
            start = datetime.strptime(root.child[0].defer, omni_format)
        result = start + delta

    if defer:
        try:
            result = datetime.strptime(defer, serial_format)
        except Exception:
            print('Defer format Example: 201809012300 your is {}.'.format(defer))
            return

    return result


def modify_omni(defer: datetime, note):
    for i, child in enumerate(root.child):
        child.defer = defer + i * w1
        child.note = note if note else child.note

def get_session_id_by_media_id(media_id: int):
    pub_date = re.search('pub_date=(\d\d\d\d)', index_url).group(1)
    season_month = re.search('season_month=(\d+)', index_url).group(1)
    page = 1
    while True:
        url = INDEX_JSON_URL.format(pub_date = pub_date, season_month= season_month, page = page)
        response = get_json_data(url)
        content = json.loads(response)
        data = content['result']['data']
        for item in data:
            if item['media_id'] == media_id:
                return item['season_id']
        total = content['result']['page']['total']
        if page * 30 >= total:
            break
        page += 1
    raise Exception("season_id for media_id={} not found".format(media_id))



def get_bangumi_detail_by_url(url: str):
    name = ''
    season_id = ''
    defer = ''
    episode = 12

    media_id_str = re.search('md(\d+)', url).group(1)
    season_id = get_session_id_by_media_id(int(media_id_str))

    json_data = get_json_data(BILIBILI_BANGUMI_DETAIL_URL.format(season_id),
                              head = 'seasonListCallback(',
                              foot = ');')
    response = json.loads(json_data)
    data = response['result']
    if 'total_count' in data:
        episode = int(data['total_count'])

    if 'title' in data:
        name = data['title']
    if 'pub_time' in data:
        defer_bilibili_str = data['pub_time']
        defer = datetime.strptime(defer_bilibili_str, '%Y-%m-%d %H:%M:%S')

    return name, season_id, defer, episode

def run(args = None, debug = False):
    global root
    parser = argparse.ArgumentParser(description = 'This is a task paper generator build for animate.')
    parser.add_argument('input', help = 'output path', nargs = '?')
    parser.add_argument('--delay', help = 'Delay mode, Format: YYYMMDDHHmm for specify time, or \d[wWdD] for delay '
                                          'relatively.', default = '')
    parser.add_argument('-d', '--defer', help = 'The datetime of animate begins.')
    parser.add_argument('-n', '--name', help = 'Name of the animate.')
    parser.add_argument('-i', '--id', help = 'id of the animate if in Bilibili.')
    parser.add_argument('-e', '--episode', help = 'The total count of animate episodes.', type = int)
    parser.add_argument('-t', '--note', help = 'Note of the animate. This will be automatically calculated if the'
                                               'animate is in blibili. Manually use this will overwrite calculated '
                                               'note.', default = [], nargs = '+')
    parser.add_argument('-u', '--url', help = 'The url of bilibili bangumi page.')
    parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s v3.3.1 by GeniusV')
    args = parser.parse_args(args)
    if len(sys.argv) < 2 and not debug:
        parser.print_usage()
        return

    if args.url:
        name, season_id, defer, e = get_bangumi_detail_by_url(args.url)
        generate(name, season_id, defer, e)
        print(root)
        return

    if args.input:
        root = Omni.read(path = args.input).child[0]

    defer = get_defer(args.delay, args.defer)

    if not args.input:
        generate(args.name, args.id, defer, args.episode, '\n'.join(args.note))
    else:
        modify_omni(defer, '\n'.join(args.note))
    print(root)


if __name__ == '__main__':
    run()
