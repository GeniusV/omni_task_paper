#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 7/29/18.

import unittest

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


