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
        from functools import reduce
        c = self.conn.cursor()
        cond = ""
        args = []
        if logger is not None or datatype is not None :
            cond = "WHERE "
        if logger is not None :
            cond += "logger = ? "
            args += str(logger)
        data=self.conn.execute("SELECT * FROM data "+cond,*args).fetchall()
        out=[]
        for row in data :
            out.append('{{"logger":{},"timestamp":{},"data":"{}"}}'.format(row[2],row[1],row[0]))
        return "[" + reduce(lambda x,y : x+","+y,out) + "]"

    def close(self):
        self.conn.commit()
        self.conn.close()
