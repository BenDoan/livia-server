#!/usr/bin/env python3

import sqlite3
import hashlib
import random
import time

from datetime import datetime

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
                        (project text, description text, date created, apikey real)''')

    def is_project(self, project):
        return len(self.conn.execute("SELECT * FROM loggers WHERE project == ?",(project,)).fetchall()) > 0

    def add_data(self,project, data):
        if self.is_project(project):
            return self.conn.execute("INSERT INTO data VALUES (?, ?, ?)", (data['data'], data['timestamp'], data['logger'])).lastrowid
        return None

    def add_logger(self,project, description):
        salt = random.random() * 100
        api_key = hashlib.sha1(str(salt).encode('utf-8') + description.encode('utf-8')).hexdigest()
        now = datetime.now()
        return self.conn.execute("INSERT INTO loggers VALUES (?, ?, ?, ?)",(project, description, now, api_key)).lastrowid

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
        for val in self.conn.execute("SELECT rowid,* FROM loggers").fetchall() if project is None else self.conn.execute("SELECT * FROM loggers WHERE (project == ?)",(project,)).fetchall():
            pattern = "%Y-%m-%d %H:%M:%S.%f"
            out.append({
                    "id":val[0],
                    "project":val[1],
                    "description":val[2],
                    "date":int(time.mktime(time.strptime(val[3], pattern))),
                    "apikey":val[4]
                })
        return out

    def close(self):
        self.conn.commit()
        self.conn.close()
