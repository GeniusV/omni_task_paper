#!/usr/bin/env python3.5
# -*-encoding: utf-8-*-

import unittest

from datetime import timedelta

from omni import *

class OmniTest(unittest.TestCase):

    def setUp(self):
        self.omni = Omni.read(path = 'omni_test_text')

    def test_output(self):
        print(self.omni)

    def test_defertime_add(self):
        print(self.omni)
        for item in self.omni.child:
            defer = item.due_time('datetime')
            print("before add: " + str(defer))

            delta = timedelta(days = 1)
            defer = defer + delta
            print("after add: " + str(defer))
            item.defer_time(defer)

        print(self.omni)






if __name__ == '__main__':
    unittest.main()




