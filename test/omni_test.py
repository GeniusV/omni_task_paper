#!/usr/bin/env python3.5
# -*-encoding: utf-8-*-

import unittest
from omni import *

class OmniTest(unittest.TestCase):

    def setUp(self):
        self.omni = Omni.read(path = 'omni_test_text')

    def test_output(self):
        print(self.omni)




