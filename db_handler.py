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
                        (data text, timestamp real, logger integer)''')
        c.execute('''CREATE TABLE IF NOT EXISTS loggers
                        (id integer primary key asc, project text, key text,description text)''')


    def insert_data(self,project,key,data):
        c = self.conn.cursor()
        if len(self.conn.execute("SELECT * FROM loggers WHERE (project == ?) AND (key == ?)",(project,key)).fetchall()) > 0 :
            self.conn.execute("INSERT INTO data VALUES (?, ?, ?)", ( json.dumps(data['data']), data['timestamp'], data['logger']))

    def add_logger(self,project,key):
        return self.conn.execute("INSERT INTO loggers (project,key) VALUES (?,?)",(project,key)).lastrowid

    def set_desc(self,logger,desc):
        self.conn.execute("UPDATE loggers SET description = ? WHERE id == ?",(logger,desc))

    def get_data(self,project,logger=None,**kwargs):
        from functools import reduce
        c = self.conn.cursor()
        cond = "WHERE "
        conds=["(data.logger = loggers.id)","(loggers.project = ?)"]
        args = [project]
        if "logger" in kwargs :
            conds.append("(data.logger = ?)")
            args.append(str(kwargs["logger"]))
        if "mintime" in kwargs :
            conds.append("(data.timestamp >= ?)")
            args.append(str(kwargs["mintime"]))
        if "maxtime" in kwargs :
            conds.append("(data.timestamp <= ?)")
            args.append(str(kwargs["maxtime"]))
        if len(conds)>0:
            cond = "WHERE "+reduce(lambda x,y : x+" AND "+y,conds)
        data=self.conn.execute("SELECT * FROM data,loggers "+cond,tuple(args)).fetchall()
        out=[]
        for row in data :
            out.append('{{"logger":{},"timestamp":{},"data":"{}"}}'.format(row[2],row[1],row[0]))
        if len(out)>0 :
            return "[" + reduce(lambda x,y : x+","+y,out) + "]"
        return "[]"
    def get_projects(self):
        out = []
        for val in self.conn.execute("SELECT DISTINCT project FROM loggers").fetchall() :
            out.append(val[0])
        return out

    def get_loggers(self,project = None):
        out = []
        for val in self.conn.execute("SELECT * FROM loggers").fetchall() if project is None else self.conn.execute("SELECT * FROM loggers WHERE (project == ?)",(project,)).fetchall():
            out.append({"id":val[0],"project":val[1],"key":val[2],"description":val[3]})
        return out

    def close(self):
        self.conn.commit()
        self.conn.close()
