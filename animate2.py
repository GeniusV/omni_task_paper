#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 3/25/18.

import json
import logging
import os
import sys
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from datetime import datetime, timedelta
from logging import Logger

import requests
from omni import Omni

original_animate_file = "2018-april-new-bangumi_raw.json"
output_file = "2018-searched-april-new-bangumi.json"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/63.0.3239.108 Safari/537.36 '
# format with bilibili bangumi animate id
BILIBILI_BANGUMI_DETAIL_URL = 'https://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver?callback=seasonListCallback&jsonp=jsonp'
# format with page
bilibili_new_bangumi_url = 'https://bangumi.bilibili.com/web_api/season/index_global?page=1&page_size=100&version=50&is_finish=50&start_year=2018&tag_id=&index_type=50&index_sort=50&area=50&quarter=2'
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s <%(filename)s> [%(funcName)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class NewBangumiManager:
    data_list: list = None
    logger: Logger = None
    file_path: str = None

    def __init__(self, file_path = '', data_list = None, logger: Logger = None,
                 log_level = logging.INFO):
        self.data_list = data_list if data_list else []
        if logger:
            self.logger = logger
            self.logger.setLevel(log_level)
        else:
            self.logger = self.get_logger(log_level)

        if not file_path == '':
            self.file_path = file_path
            self.data_list = self.read_json(file_path)
        else:
            self.file_path = "result.json"

    @staticmethod
    def read_json(path):
        with open(path, 'r', encoding = 'utf-8') as f:
            json_string = f.read()
        return json.loads(json_string)

    @staticmethod
    def write_json(path, object):
        with open(path, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(object, ensure_ascii = False, indent = 2))

    def __str__(self):
        return json.dumps(self.data_list, ensure_ascii = False, indent = 2)

    def save(self, path = ''):
        save_path = path if path else self.file_path
        self.write_json(save_path, self.data_list)

    @staticmethod
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

    def if_need_to_update(self):
        for item in self.data_list:
            if item['inBilibili'] and not item['note'] and item['defer'] and item['e']:
                return True
        return False

    def init_new_bangumi_json(self, bilibili_repo_url, check_length = 3, raw_list_file = ''):
        """
        This method will compare my bangumi list, with bangumi list in bilibili.com

        :type bilibili_repo_url str
        :param bilibili_repo_url: This url is used to query new bangumi json data.
            The url can be found in https://bangumi.bilibili.com/anime/index.
            The url should look like https://bangumi.bilibili.com/web_api/season/index_global?page=1&page_size=100&version=50&is_finish=50&start_year=2018&tag_id=&index_type=50&index_sort=50&area=50&quarter=2

        :type raw_list_file str
        :param raw_list_file: the file include your animate list, which should look like this:
            [
              "甜蜜惩罚",
              "ALICE or ALICE",
              "立花馆恋爱三角铃",
              ...
            ]

        :type output_file_path str
        :param output_file_path: The file will output final processed data, which will look like this:
            [
              {
                "name": "命运石之门0",
                "inBilibili": false,
                "bilibili_url": "",
                "bilibili_id": ""
              },
              ...
            ]

        :type check_length int
        :param check_length: This method will check if first n char of every bangumi name in bangumi title from bilibili.
            n is the check_length.
            If check_length is set too big, the match will be too insensitive and this will miss bangumis exist in bilibili.
            If check_length is set too small, the match will be too sensitive and some bangumi in bilibili may be mathed for
            multi times. So your result file appears duplicated records, consider if the check_length is set too small.
        """
        # get first page
        if "bangumi.bilibili.com/web_api/season/index_global" not in bilibili_repo_url:
            raise ValueError(
                "bilibili_repo_url should like https://bangumi.bilibili.com/web_api/season/index_global?page=1"
                "&page_size=100&version=50&is_finish=50&start_year=2018&tag_id=&index_type=50&index_sort=50&"
                "area=50&quarter=2" + bilibili_repo_url)
        self.data_list = self.read_json(raw_list_file) if raw_list_file else print(end = '')
        raw = self.get_json_data(bilibili_repo_url)
        object_data = json.loads(raw)
        raw_bangumis = object_data['result']['list']
        my_result_list = []
        for my in self.data_list:
            new = {
                'name': my,
                'inBilibili': False,
                'bilibili_url': "",
                'bilibili_id': "",
                "note": "",
                "e": 12,
                "defer": ""
            }
            for item in raw_bangumis:
                if my[:check_length] in item['title'] or my[-check_length:] in item['title']:

                    self.logger.info("{} is found, initing...".format(item['title']))

                    new['name'] = item['title']
                    new['inBilibili'] = True
                    new['bilibili_url'] = item['url']
                    new['bilibili_id'] = item['season_id']
            my_result_list.append(new)
        self.data_list = my_result_list

    def update_bangumi(self):
        update_bangumi_list = []
        for item in self.data_list:
            if item['note'] == '' and item['inBilibili'] is True:
                update_bangumi_list.append(item)

        with ThreadPoolExecutor(max_workers = 20) as executor:
            futures = {executor.submit(self.query_and_update_bangumi, data): data for data in update_bangumi_list}
            for future in as_completed(futures):  # type: Future
                data_set = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.logger.error("{} generate an error: {}".format(data_set['name'], e))
                else:
                    self.logger.debug("{} done".format(data_set['name']))

    def query_and_update_bangumi(self, item: dir):
        json_data = self.get_json_data(BILIBILI_BANGUMI_DETAIL_URL.format(item['bilibili_id']),
                                       head = 'seasonListCallback(',
                                       foot = ');')
        result = json.loads(json_data)
        data = result['result']
        release_time = data['pub_time']  # type: str

        if not release_time.endswith('00:00:01'):
            release_time = datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
            release_time = release_time.strftime('%Y%m%d%H%M')
            item['defer'] = release_time
            self.logger.info('"{}" defer is set to {}'.format(item['name'], release_time))

        if 'total_count' in data:
            item['e'] = int(data['total_count'])

    @staticmethod
    def get_logger(level):
        LOG_FORMAT = "%(asctime)s - %(levelname)s <%(filename)s> [%(funcName)s]: %(message)s"
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        logger = logging.getLogger('DefaultLogger')

        logger.setLevel(level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(console_handler)
        return logger

    def generate_omni(self, animate_list):
        root = Omni()
        for item in animate_list:
            omni = Omni()
            omni.name = item['name']
            self.logger.debug('generating animate: "{}"'.format(item['name']))
            omni.note = item['bilibili_url']
            omni.parallel = True
            omni.auto_done = True
            omni.context = 'watch : excellent animation'
            if len(item['defer']) < 12 or 'out' in item:
                self.logger.error('"{}" defer "{}" format is not correct.'.format(item['name'], item['defer']))
            try:
                start_time = datetime.strptime(item['defer'], '%Y%m%d%H%M%S')
            except ValueError:
                raise ValueError('defer time format error:{}'.format(item))
            week = timedelta(weeks = 1)
            for i in range(item['e']):
                child_omni = Omni()
                child_omni.name = omni.name + ' - ' + str(i + 1)
                child_omni.note = omni.note
                child_omni.defer = start_time + week * i
                child_omni.context = 'excellent animation'
                omni.append(child_omni)
            root.append(omni)
        return root

    def generate_animate_not_in_bilibili(self):
        return self.generate_omni([item for item in self.data_list if not item['inBilibili']])

    def generate_animate_in_bilibili(self, update_data_status = False):
        ready_list = [item for item in self.data_list if item['inBilibili'] and not item['note'] and item['defer'] and item['e']]
        self.logger.debug("ready to generate animate in bilibili: {}".format(ready_list))
        if update_data_status:
            self.logger.debug("update_data_status is on...")
            for item in ready_list:
                item['note'] = item['bilibili_url']
                self.logger.debug('"{}" note is updated: "{}"'.format(item['name'], item['note']))
        return self.generate_omni(ready_list)

def run_auto():
    try:
        a = NewBangumiManager(
            file_path = '/Users/GeniusV/Documents/pythonProject/omnifocus/2018-searched-april-new-bangumi.json')
        a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "/Users/GeniusV/Documents/pythonProject/omnifocus/2018-april-new-bangumi_raw.json")
        a.update_bangumi()
        if a.if_need_to_update():
            os.system('''
                osascript -e 'display notification "Bangumi Updated" with title "from Animate2.py"'
            ''')
    except Exception as e:
        os.system('''
            osascript -e 'display notification "Bangumi Updated Error!!!!" with title "from Animate2.py"'
        ''')

def run_script():
    a = NewBangumiManager(
        file_path = '2018-searched-april-new-bangumi.json')
    # a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "2018-april-new-bangumi_raw.json")
    a.update_bangumi()
    print(a.generate_animate_in_bilibili(update_data_status = True))
    # print(a.if_need_to_update())
    a.save()

def reset():
    a = NewBangumiManager(
        file_path = '2018-searched-april-new-bangumi.json')
    a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "2018-april-new-bangumi_raw.json")
    a.save()


if __name__ == '__main__':
    # run_auto()
    run_script()
    # reset()
