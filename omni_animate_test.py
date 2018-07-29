#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 7/29/18.

import unittest

import omni_animate3
from omnifocus.omni import Omni


class AnimateTest(unittest.TestCase):

    def tearDown(self):
        omni_animate3.root = Omni()

    def test_generate_defer(self):
        omni_animate3.run('-n test_name -d 201809010000 -e 15 -t http://test.com'.split())

    def test_generate_delay(self):
        omni_animate3.run('-n test_name --delay 2d -e 15 -t http://test.com'.split())

    def test_modify_defer(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni -t http://test.com'.split())

    def test_modify_delay(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni --delay 2w -t http://test.com'.split())

    def test_no_args(self):
        omni_animate3.run(''.split())

    def test_input_only(self):
        omni_animate3.run('/Users/GeniusV/Desktop/omni'.split())


