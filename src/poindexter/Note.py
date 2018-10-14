#! /usr/bin/env python
# -*- coding: utf-8 -*-


format_dir = r'(\w+)\s+(\d)(\d)\s+(\w+),\s+(\w+\s*\w*),\s+(\w+)\s+(\w+),\s+(\d+)'


class Note:
    def __init__(self, faculty, graduate, course_name, course_year, lecturer_name, total_year, semester):
        self.faculty = faculty
        self.graduate = graduate
        self.course_name = course_name
        self.course_year = course_year
        self.lecturer_name = lecturer_name
        self.total_year = total_year
        self.semester = semester

    def __str__(self):
        return """'%s', '%s', '%s', %s, '%s', %s, %s""" % (self.faculty, self.graduate, self.course_name,
                                                           self.course_year, self.lecturer_name, self.total_year,
                                                           self.semester)

    @staticmethod
    def fromList(note):
        return Note(note[0], note[3], note[4], note[1], "%s %s" % (note[5], note[6]),
                    note[7], note[2])
