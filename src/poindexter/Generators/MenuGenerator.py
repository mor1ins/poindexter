#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Abstructions.Generator import IGenerator
import dependency
import os


class MenuTree:
    def __init__(self):
        self.hierarchy = dict()

    def add(self, elem):
        if len(elem) == 0:
            return self
        if not self.hierarchy.keys().__contains__(elem[0]):
            self.hierarchy[elem[0]] = MenuTree()
            self.hierarchy[elem[0]].add(elem[1:])
        else:
            self.hierarchy[elem[0]].add(elem[1:])

    def tree2str(self):
        tree = ""
        for key in self.hierarchy.keys():
            if len(self.hierarchy[key].hierarchy) == 0:
                tree += key
            else:
                tree += "{{Hider|%s\n" % key
                tree += self.hierarchy[key].tree2str()
                tree += "\n}}\n"
        return tree


def transform(note):
    return note[1], note[0], "[{}|{}{}. {} {} {}]".format(note[7], note[3], note[6], note[4], note[2], note[5])


class MenuGenerator(IGenerator):
    def __init__(self):
        self.db = dependency.global_db

    def generate(self, source, destination):
        notes = self.db.select_all()
        menu = MenuTree()
        for note in notes:
            menu.add(transform(note))

        if os.path.exists(destination):
            os.remove(destination)
        file = open(destination, "w+")
        file.write(menu.tree2str())
        file.close()
