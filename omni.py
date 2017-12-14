#!/usr/bin/env python3.5
# -*-encoding: utf-8-*-
import re
from datetime import datetime

serial_format = '%Y%m%d%H%M'
omni_format = '%Y-%m-%d %H:%M'


class Omni():
    def __init__(self):
        self.child = []  # type: list[Omni]
        self.level = -1
        self.name = ''  # type: str
        self.parallel = False  # type: bool
        self.auto_done = False  # type: bool
        self.context = ''  # type: str
        self.defer = ''  # type: str
        self.flagged = False  # type: bool
        self.note = ''  # type: str
        self.due = ''  # type: str
        self.parent = None  # type: Omni

    def __str__(self):
        return self.format_string()

    def get_level(self, line):
        """

        :type line: str
        """
        ct = 0
        while line.startswith('    '):
            line = line[4:]
            ct += 1
        return ct

    @classmethod
    def read(cls, str = '', path = ''):
        omni = Omni()
        if not path == '':
            with open(path, 'r', encoding = 'utf-8') as f:
                str = f.read()
        lines = str.split('\n')
        index = 0
        parent = omni
        while index < len(lines):
            if lines[index] == '':
                break
            note, next_index = omni.get_note(lines, index)
            omni = omni.create_new(lines[index], omni.get_level(lines[index]), note)
            index = next_index
            if omni.level <= parent.level:
                parent = omni.get_parent(parent)
            omni.parent = parent
            parent.child.append(omni)
            parent = omni
        return omni

    def get_parent(self, node):
        """
        :type node: Omni
        """
        level = node.level - 1
        if level < 0:
            return self

        while not node.level == level:
            node = node.parent
        return node

    def get_note(self, lines, index):
        note = ''
        pre = ''
        for i in range(0, self.get_level(lines[index])):
            pre += '    '
        while index + 1 < len(lines) and not lines[index + 1].strip(' ').startswith('-'):
            index += 1
            note += lines[index].strip(' ')
            note += '\n'
        return note[:-1], index + 1

    def create_new(self, line, level, note = ''):
        omni = Omni()
        omni.name = re.search("- (.*?) @", line).group(1)
        omni.auto_done = re.search(" @autodone\((.*?)\) ", line).group(1)
        if '@context' in line:
            omni.context = re.search(" @context\((.*?)\)", line).group(1)
        if '@defer' in line:
            omni.defer = re.search(" @defer\((.*?)\)", line).group(1)
        omni.parallel = re.search(" @parallel\((.*?)\)", line).group(1)
        if '@due' in line:
            omni.due = re.search(" @due\((.*?)\)", line).group(1)
        omni.level = level
        omni.note = note
        if line.find('@flagged') < 0:
            omni.flagged = False
        return omni

    def format_string(self, recursion = True, path = '', string = ''):
        if self.name:
            pre = ''
            if self.flagged:
                flagged = '@flagged'
            else:
                flagged = ''
            for index in range(0, self.level):
                pre += '    '
            string += '{}- {} @parallel({}) @autodone({}) @due({}) @defer({}) @context({}) {}\n'.format(pre, self.name,
                                                                                                        self.parallel,
                                                                                                        self.auto_done,
                                                                                                        self.due,
                                                                                                        self.defer,
                                                                                                        self.context,
                                                                                                        flagged)
            if self.note != '':
                string += pre + '    ' + self.note
        if recursion:
            for item in self.child:
                string += item.format_string(recursion = True)
        return string

    def update(self, name = '', defer = '', due = '', context = '', flagged = '', parallel = '', autodone = '',
               note = ''):
        if not name == '':
            self.name = name
        if not defer == '':
            self.defer = defer
        if not due == '':
            self.due = due
        if not context == '':
            self.context = context
        if not flagged == '' and isinstance(flagged, bool):
            self.flagged = flagged
        if not parallel == '' and isinstance(parallel, bool):
            self.parallel = parallel
        if not autodone == '' and isinstance(autodone, bool):
            self.auto_done = autodone
        if not note == '':
            self.note = note

    def append(self, omni):
        """

        :type omni: Omni
        """
        self.child.append(omni)
        omni.parent = self
        omni.level = self.level + 1
        self.check_level()

    def check_level(self, recursion = True):
        for item in self.child:
            item.level = self.level + 1
            if recursion:
                item.check_level(recursion)

    def defer_time(self, *args):
        """
        Return the defer time of the object if pass nothing.
        Return a datetime format defer time of the object if pass 'datetime' str.
        Pass a datetime or formatted str to set the defer time of the object.
        :type datetime_or_str: datetime | str
        """
        for item in args:
            if item == 'datetime':
                return datetime.strptime(self.defer, omni_format)
            if isinstance(item, datetime):
                self.defer = item.strftime(omni_format)
                return
            if isinstance(item, str):
                self.defer = item
                return
        return self.defer

    def due_time(self, *args):
        """
        Return the due time of the object if pass nothing.
        Return a datetime format due time of the object if pass 'datetime' str.
        Pass a datetime or formatted str to set the due time of the object.
        :type datetime_or_str: datetime | str
        """
        for item in args:
            if item == 'datetime':
                return datetime.strptime(self.defer, omni_format)
            if isinstance(item, datetime):
                self.due = item.strftime(omni_format)
                return
            if isinstance(item, str):
                self.due = item
                return
        return self.due


if __name__ == '__main__':
    # datetime and timedelta
    # time = datetime.strptime("201712092300", strp_format)
    # date_string = time.strftime(strf_format)
    # time_delta = timedelta(days = 1)

    omni = Omni()
    omni.read(path = '/Users/GeniusV/Desktop/omni')
    # write in here



    with open('/Users/GeniusV/Desktop/omni-result', 'w', encoding = 'utf-8') as f:
        f.write(omni.format_string())
