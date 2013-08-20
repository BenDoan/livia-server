#!/usr/bin/env python3

import sqlite3

class db_handler:
    def __init__(self, name):
        self.name = name
        self.conn = self.get_db()
        self.setup()

    def get_db(self):
        return sqlite3.connect(self.name)

    def setup(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data
                        (data text, timestamp real, logger real)''')

    def insert_data(self, data):
        c = self.conn.cursor()
        self.conn.execute("INSERT INTO data VALUES (?, ?, ?)", (data['data'], data['timestamp'], data['logger']))

    def get_data(self,datatype=None,logger=None):
        c = self.conn.cursor()

        self.conn.execute("SELECT * FROM data WHERE logger = {}".format(logger))

    def close(self):
        self.conn.commit()
        self.conn.close()
