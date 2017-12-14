#!/usr/bin/env python3.5
# -*-encoding: utf-8-*-
import datetime
import os
import re

import pyperclip as pyperclip


class Work:
    """
    This is the work class of the OmniTaskPaper.
    """

    def __init__(self):
        self.state = AnimateState()
        self.list = []
        self.current_line = ""
        self.current_animate = None  # type: Animate
        self.current_child = None  # type: AnimateChild

    def read(self, path = "/Users/GeniusV/Desktop/omni.txt"):
        """
        This method read the OmniTaskPaper file.
        :type path: str
        :param path: the path of the file, default: "/Users/GeniusV/Desktop/omni.txt"
        :return:
        """
        with open(path, encoding = "utf-8") as file:
            for line in file:
                self.current_line = line[:-1]
                self.state.read(self)
        print(self.list)

    def add(self, name, defer, note, num = 12, next = 1, replan = False, context = 'watch : excellent animation'):

        self.current_animate = Animate()
        self.list.append(self.current_animate)
        self.current_animate.name = name
        self.current_animate.parallel = True
        self.current_animate.autodone = True
        self.current_animate.context = context
        for i in range(next, num + 1):
            self.current_child = AnimateChild()
            self.current_animate.animate_children.append(self.current_child)
            self.current_child.name = name + "-" + str(i)
            self.current_child.e = i
            self.current_child.parallel = True
            self.current_child.autodone = False
            self.current_child.context = context
            self.current_child.note = note
            if replan:
                self.current_child.defer = self.__get_time(defer, i - next + 1)
            else:
                self.current_child.defer = self.__get_time(defer, i)

    def update(self, name, new_name = "", defer = "", note = "", num = 0, next = 0, replan = True, context = ''):
        template = None  # type: AnimateChild
        for item in self.list:  # type: Animate
            if item.name == name:
                template = self.__get_deffer(item)
                template.name = item.name
                self.list.remove(item)
        if not template:
            raise Exception("No Such Animate: [{}]".format(name))
        if not new_name == "":
            template.name = new_name
        if not defer == "":
            template.defer = defer
        if not num == 0:
            template.e = num
        if not note == "":
            template.note = note
        if not context == "":
            template.context = context
        if not next == 0:
            template.next = next
        self.add(template.name, template.defer, template.note, template.e, template.next, replan, template.context)

    @staticmethod
    def __get_deffer(animate):
        """
        :type animate: Animate
        :param animate:
        :return:
        """
        biggest = 100000
        value = animate.animate_children[0]  # type: AnimateChild
        for child in animate.animate_children:  # type: AnimateChild
            if child.e < biggest:
                biggest = child.e
                value.defer = child.defer
                value.next = child.e
            if child.e > value.e:
                value.e = child.e
        return value

    @staticmethod
    def __get_time(start_time, num):
        """
        :type start_time: str
        :type num: int
        """
        date = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        date = date + datetime.timedelta(days = 7 * (num - 1))
        return str(date.strftime("%Y-%m-%d %H:%M"))

    def output(self):
        with open("/Users/GeniusV/Desktop/omni-animate-result-updated.txt", "w", encoding = "utf-8") as file:
            file.write("- Animate @parallel(true) @autodone(false) @context(watch)\n")
            for item in self.list:  # type: Animate
                file.write("    - {} @parallel(true) @autodone(true) @context({})".format(item.name, item.context))
                if item.defer:
                    file.write(" @defer({})".format(item.defer))
                file.write("\n")
                for child in item.animate_children:  # type: AnimateChild
                    file.write(
                        "         -{} @parallel(true) @autodone(false) @context({}) @defer({})\n".format(child.name,
                                                                                                         child.context,
                                                                                                         child.defer))
                    file.write("            {}\n".format(child.note))

class State:
    def __init__(self):
        pass

    def read(self, work):
        pass


class NoteState(State):
    def __init__(self):
        super().__init__()

    def read(self, work):
        """
        :type work: Work
        :param work:
        :return:
        """
        if work.current_line.startswith("    - "):
            work.state = AnimateState()
            work.state.read(work)
        elif work.current_line.startswith("        - "):
            work.state = ChildState()
            work.state.read(work)
        elif work.current_line.startswith("-"):
            pass
        elif work.current_line == "":
            pass
        else:
            if not work.current_child.note == "":
                work.current_child.note += "\n"
            work.current_child.note += work.current_line


class AnimateState(State):
    def __init__(self):
        super().__init__()

    def read(self, work):
        """
        :type work: Work
        :param work:
        :return:
        """
        if work.current_line.startswith("    - "):
            work.current_animate = Animate()
            work.list.append(work.current_animate)
            work.current_animate.name = re.search("- (.*?) @", work.current_line).group(1)
            work.current_animate.parallel = re.search(" @parallel\((.*?)\) ", work.current_line).group(1)
            work.current_animate.autodone = re.search(" @autodone\((.*?)\) ", work.current_line).group(1)
            work.current_animate.context = re.search(" @context\((.*?)\)", work.current_line).group(1)
            defer = re.search(" @defer\((.*?)\)", work.current_line)
            if defer:
                work.current_animate.defer = defer.group(1)
            work.state = ChildState()
        elif work.current_line.startswith("        - "):
            raise Exception("except AnimateState, but the current line is the child line")
        elif work.current_line.startswith("-"):
            pass
        else:
            work.state = NoteState()
            work.state.read(work)


class ChildState(State):
    def __init__(self):
        super().__init__()

    def read(self, work):
        """
        :type work: Work
        :param work:
        :return:
        """
        if work.current_line.startswith("        - "):
            work.current_child = AnimateChild()
            work.current_animate.animate_children.append(work.current_child)
            work.current_child.name = re.search("- (.*?) @", work.current_line).group(1)
            work.current_child.e = int(re.search("-(\d*) @", work.current_line).group(1))
            work.current_child.autodone = re.search(" @autodone\((.*?)\) ", work.current_line).group(1)
            work.current_child.context = re.search(" @context\((.*?)\)", work.current_line).group(1)
            work.current_child.defer = re.search(" @defer\((.*?)\)", work.current_line).group(1)
            work.current_child.parallel = re.search(" @parallel\((.*?)\)", work.current_line).group(1)
        elif work.current_line.startswith("    - "):
            work.state = AnimateState()
            work.state.read(work)
        elif work.current_line.startswith("-"):
            pass
        else:
            work.state = NoteState()
            work.state.read(work)


class Animate:
    def __init__(self):
        self.name = None  # type: str
        self.parallel = None  # type: bool
        self.autodone = None  # type: bool
        self.context = None  # type: str
        self.animate_children = []  # type: list
        self.defer = None  # type: str


class AnimateChild:
    def __init__(self):
        self.name = None  # type: str
        self.e = None  # type: int
        self.parallel = None  # type: str
        self.autodone = None  # type: bool
        self.context = None  # type: str
        self.defer = None  # type: str
        self.note = ""  # type: str


if __name__ == '__main__':
    w = Work()
    w.read()
    w.update("网络胜利组", defer = '2017-10-28 01:00')
    w.output()
