#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

create_query = 'CREATE TABLE %s (%s)'
insert_query = 'INSERT INTO %s VALUES (%s)'
select_query = 'SELECT %s FROM %s %s'
trans_set_query = 'SET TRANSACTION %s'
trans_autocommit_query = 'SET autocommit=&d'


class OutlineDatabase:
    def __init__(self, server, user, passwd, name_db):
        self.__server = server
        self.__user = user
        self.__passwd = passwd
        self.__name_db = name_db
        self.__db = None
        self.__cursor = None

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    def connect(self):
        self.db = sqlite3.connect(self.__server,
                                  self.__user,
                                  self.__passwd,
                                  self.__name_db)

    def close(self):
        self.db.close()

    def set_transaction(self, params):
        pass

    def autocommit_off(self):
        self.execute(trans_autocommit_query, None)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def cursor(self):
        self.__cursor = self.db.cursor()
        return self.__cursor

    def execute(self, sql, params):
        query = ""
        if params is not None:
            query = "%s %s"
        else:
            query = "%s"
        self.cursor().execute(query % (sql, params))

    def fetchall(self):
        return self.cursor().fetchall()

    def fetchone(self):
        return self.cursor().fetchone()

    def create_table(self, table, rows):
        query = create_query % (table, rows)
        self.execute(query, None)

    def insert_into(self, table, values):
        query = insert_query % (table, values)
        self.execute(query, None)

    def select_from(self, select, table, params):
        query = select_query % (select, table)
        additionals = None
        self.execute(query, additionals)


if __name__="__main__":
    pass