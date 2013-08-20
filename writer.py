#!/usr/bin/env python3

import sqlite3

class log_writer():
    def __init__(self):
        self.conn = self.get_db()
        #self.setup()


    def get_db(self):
        return sqlite3.connect("data.db")

    def setup(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data
                        (data text, timestamp real, logger real)''')

    def insert_data(self, data):
        c = self.conn.cursor()
        self.conn.execute("INSERT INTO data VALUES ({}, {}, {})".format(data['data'], data['timestamp'], data['logger']))

    def close(self):
        self.conn.commit()
        self.conn.close()
