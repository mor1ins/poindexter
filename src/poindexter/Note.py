#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
from log import logable

format_dir = r'(\w+)\s+(\d)(\d)\s+(\w+),\s+(\w+\s*\w*),\s+(\w+)\s+(\w+),\s+(\d+)'


def is_satisfy(note):
    return note is None


class Note:
    def __init__(self, faculty, graduate, course_name, course_year, lecturer_name, total_year, semester, rand_id):
        self.faculty = faculty
        self.graduate = graduate
        self.course_name = course_name
        self.course_year = course_year
        self.lecturer_name = lecturer_name
        self.total_year = total_year
        self.semester = semester
        self.url = "%s" % rand_id

    def __str__(self):
        return """'%s', '%s', '%s', %s, '%s', %s, %s, '%s'""" % (self.faculty, self.graduate, self.course_name,
                                                                 self.course_year, self.lecturer_name, self.total_year,
                                                                 self.semester, self.url)

    @staticmethod
    def from_list(title: str, rand):
        note = re.findall(format_dir, title, re.U)[0]
        print("begin")
        if not (len(note) == 8 and isinstance(note[0], str) and isinstance(note[1], str)
                and isinstance(note[2], str) and isinstance(note[3], str)
                and isinstance(note[4], str) and isinstance(note[5], str)
                and isinstance(note[6], str) and isinstance(note[7], str)):
            return None

        return Note(note[0], note[3], note[4], note[1], "%s %s" % (note[5], note[6]),
                    note[7], note[2], rand)
