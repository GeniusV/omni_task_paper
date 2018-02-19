#!/usr/bin/env python3.5
# -*-encoding: utf-8-*-

import unittest

from datetime import timedelta

from omni import *


class OmniTest(unittest.TestCase):
    def setUp(self):
        # default raw data
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

    def test_iterable(self):
        for item in self.omni:
            print(item)

    def test_create_new(self):
        root = Omni()
        name = 'part-'
        one_day = timedelta(days = 1)
        today = Omni.get_default_defer_datetime()
        for i in range(11):
            omni = Omni()
            omni.name = name + str(i + 1)
            omni.defer_time(today + one_day * i)
            root.append(omni)
        print(root)

    def test_get_default_due_datetime(self):
        print(Omni.get_default_due_datetime())

    def test_get_default_defer_datetime(self):
        print(Omni.get_default_defer_datetime())

    def test_getItem(self):
        print(self.omni[0])


if __name__ == '__main__':
    unittest.main()
