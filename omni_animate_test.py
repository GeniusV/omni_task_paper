#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 7/29/18.
import re
import unittest
from datetime import datetime

import omni_animate3
from omnifocus.omni import Omni


class AnimateTest(unittest.TestCase):
    """
    To run these tests, there must be a file /Users/GeniusV/Desktop/omni with content like this:
    - 汤摇庄的幽奈小姐  @parallel(true) @autodone(false) @context(watch : excellent animation)
        - 汤摇庄的幽奈小姐  - 3 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-07-29 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 4 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-08-05 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 5 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-08-12 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 6 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-08-19 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 7 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-08-26 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 8 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-09-02 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 9 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-09-09 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 10 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-09-16 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 11 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-09-23 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/

        - 汤摇庄的幽奈小姐  - 12 @parallel(false) @autodone(false) @context(watch : excellent animation) @defer(2018-09-30 00:00)
            http://www.dilidili.wang/anime/tyzdyntx/
    """


    def tearDown(self):
        omni_animate3.root = Omni()

    def test_generate_defer(self):
        omni_animate3.run('-n test_name -d 201809010000 -e 15 -t http://test.com'.split(), debug = True)

    def test_generate_delay(self):
        omni_animate3.run('-n test_name --delay 2d -e 15 -t http://test.com'.split(), debug = True)

    def test_modify_defer(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni -t http://test.com'.split(), debug = True)

    def test_modify_delay(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni --delay 2w -t http://test.com'.split(), debug = True)

    def test_modify_defer_reserve_note(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni -d 201807290000'.split(), debug = True)

    def test_no_args(self):
        omni_animate3.run(''.split(), debug = True)

    def test_input_only(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni'.split(), debug = True)

    def test_note(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni -t test test'.split(), debug = True)

    def test_help(self):
        with self.assertRaises(SystemExit):
            omni_animate3.run('-h'.split(), debug = True)

    def test_regex(self):
        pub_date = re.search('pub_date=(\d\d\d\d)', omni_animate3.index_url).group(1)
        season_month = re.search('season_month=(\d+)', omni_animate3.index_url).group(1)

        print(pub_date, season_month)


    def test_get_season_id(self):
        season_id = omni_animate3.get_session_id_by_media_id(12392)
        print(season_id)


    def test_datetime_format(self):
        date_str = '2018-07-10 22:30:00'
        result = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        print(result)

    def test_get_bangumi_detail_by_url(self):
        result = omni_animate3.get_bangumi_detail_by_url('https://www.bilibili.com/bangumi/media/md134912/?spm_id_from=666.10.bangumi_detail.1')
        print(result)

    def test_generate_by_url(self):
        omni_animate3.run('-u https://www.bilibili.com/bangumi/media/md139252/?spm_id_from=666.10.bangumi_detail.2'.split(), debug = True)

    def test_increase_episode(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni.txt -e 15 -d 201809011100'.split(), debug = True)