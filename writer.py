#!/usr/bin/env python3

import sqlite3

def get_data():
    return {
                "timestamp":1376948822,
                "logger":1,
                "data":"5000"
            }


def get_db():
    return sqlite3.connect("data.db")

def setup_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                    (data text, timestamp real, logger real)''')

def insert_data(conn, data):
    conn.execute("INSERT INTO data VALUES ({}, {}, {})".format(data['data'], data['timestamp'], data['logger']))

def close_db(conn):
    conn.commit()
    conn.close()

conn = get_db()
setup_db(conn)
insert_data(conn, get_data())
close_db(conn)
