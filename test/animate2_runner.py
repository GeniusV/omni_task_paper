#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 3/31/18.

import unittest

from animate2 import *


class Animate2Runner(unittest.TestCase):
    def test_run_script_no_update(self):
        a = NewBangumiManager(
            file_path = '../2018-searched-april-new-bangumi.json', log_level = logging.DEBUG)
        # a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "2018-april-new-bangumi_raw.json")
        a.update_bangumi()
        print(a.generate_animate_in_bilibili(update_data_status = False))
        # print(a.if_need_to_update())
        a.save()

    def test_run_script_update(self):
        a = NewBangumiManager(
            file_path = '../2018-searched-april-new-bangumi.json')
        # a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "2018-april-new-bangumi_raw.json")
        a.update_bangumi()
        print(a.generate_animate_in_bilibili(update_data_status = True))
        # print(a.if_need_to_update())
        a.save()

    def test_reset(self):
        a = NewBangumiManager(
            file_path = '../2018-searched-april-new-bangumi.json')
        a.init_new_bangumi_json(bilibili_new_bangumi_url, raw_list_file = "../2018-april-new-bangumi_raw.json")
        a.save()

if __name__ == '__main__':
    unittest.main()
