#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from sqlalchemy import create_engine

DB_NAME = "sqlite"
TABLE_NAME = "notes"
DB_NOTES_PATH = "../../../%s.db" % TABLE_NAME
CONNECTING_STRING = "%s:///%s" % (DB_NAME, DB_NOTES_PATH)
notes_fields = """
    note_id integer primary key,
    faculty varchar,
    graduate varchar,
    course_name varchar,
    study_year integer,
    lecture_name varchar,
    total_year integer,
    semester integer
"""
inserting_fields = """
    faculty, graduate, course_name, study_year, lecture_name, total_year, semester
"""
create_table_query = "create table %s (%s)" % (TABLE_NAME, notes_fields)
insert_query = 'insert into %s(%s) values (%s)' % (TABLE_NAME, inserting_fields, "%s")
select_query = 'select %s from %s' % ("%s", TABLE_NAME)


# trans_set_query = 'SET TRANSACTION %s'
# trans_autocommit_query = 'SET autocommit=&d'


class NotesDB:
    def __init__(self):
        self.engine = create_engine(CONNECTING_STRING)

    def create_table(self):
        self.engine.execute(create_table_query)

    def remove_table(self):
        if os.path.exists(DB_NOTES_PATH):
            os.remove(DB_NOTES_PATH)

    def insert_into(self, values):
        query = insert_query % values
        self.engine.execute(query)

    def selectall(self):
        result = self.engine.execute(select_query % inserting_fields)
        return result.fetchall()


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
        return """'%s', '%s', '%s', %s, '%s', %s, %s""" % (self.faculty, self.graduate, self.course_name, self.course_year,
                                                          self.lecturer_name, self.total_year, self.semester)




if __name__ == "__main__":

    # notes = [
    #     Note("магистратура", "МОЗИ", 3, "Пилиди", 2017, 2),
    #     Note('магистратура', 'Компиляторы', 3, 'Михалкович', 2017, 2)
    # ]

    db = NotesDB()
    db.remove_table()
    db.create_table()

    dirs = os.listdir("../../../out")
    for dir in dirs:
        matches = re.findall(r'(\w+)\s+(\d)(\d)\s+(\w+),\s+(\w+\s*\w*),\s+(\w+)\s+(\w+),\s+(\d+)', dir, re.U)
        if len(matches) > 0:
            note = matches[0]
            db.insert_into(Note(note[0], note[3], note[4], note[1], "%s %s" % (note[5], note[6]), note[7], note[2]).__str__())

    for note in db.selectall():
        print(note)

    #
    # @property
    # def db(self):
    #     return self.__db
    #
    # @db.setter
    # def db(self, value):
    #     self.__db = value
    #
    # def connect(self):
    #     self.db = sqlite3.connect(self.__server,
    #                               self.__user,
    #                               self.__passwd,
    #                               self.__name_db)
    #
    # def close(self):
    #     self.db.close()
    #
    # def set_transaction(self, params):
    #     pass
    #
    # def autocommit_off(self):
    #     self.execute(trans_autocommit_query, None)
    #
    # def commit(self):
    #     self.db.commit()
    #
    # def rollback(self):
    #     self.db.rollback()
    #
    # def cursor(self):
    #     self.__cursor = self.db.cursor()
    #     return self.__cursor
    #
    # def execute(self, sql, params):
    #     query = ""
    #     if params is not None:
    #         query = "%s %s"
    #     else:
    #         query = "%s"
    #     self.cursor().execute(query % (sql, params))
    #
    # def fetchall(self):
    #     return self.cursor().fetchall()
    #
    # def fetchone(self):
    #     return self.cursor().fetchone()

    # query = create_query % (table, rows)
    # self.execute(query, None)

    # def select_from(self, select, table, params):
    #     query = select_query % (select, table)
    #     additionals = None
    #     self.execute(query, additionals)
