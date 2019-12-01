import sqlite3
from scrape import scrape_amz
import datetime as dt

def add(asin):
    #for now trust that the ASIN is correct
    conn = sqlite3.connect(r"db\ASIN.db")
    c = conn.cursor()
    t = (asin,)
    q = "select * from asin where asin=(?)"
    c.execute(q, t)
    if c.fetchone():
        print(asin + " already exists in database")
    else:
        q = "create table if not exists asin (asin TEXT)"
        c.execute(q)
        q = "insert into asin values (?)"
        c.execute(q, t)
        print(asin + " added to database")
        conn.commit()
    conn.close()

def remove(asin):
    if asin == "asin":
        print("Invalid")
    else:
        conn = sqlite3.connect(r"db\ASIN.db")
        c = conn.cursor()
        t = (asin,)
        q = "select * from asin where asin=(?)"
        c.execute(q, t)
        if c.fetchone():
            t = (asin,)
            q = "drop table if exists " + asin + "_Product_html"
            c.execute(q)
            q = "drop table if exists " + asin + "_ProductCart_html"
            c.execute(q)
            q = "delete from asin where asin=(?)"
            c.execute(q, t)
            print(asin + " removed from database")
            conn.commit()
        else:
            print(asin + " not in database")
        conn.close()


def list():
    conn = sqlite3.connect(r"db\ASIN.db")
    c = conn.cursor()
    q = "select * from asin"
    c.execute(q)
    asins = c.fetchall()
    print("ASINs in database - Qty(" + str(len(asins)) + ")")
    for asin in asins:
        print(asin[0])
    conn.close()

def scrape():
    conn = sqlite3.connect(r"db\ASIN.db")
    c = conn.cursor()
    q = "select * from asin"
    c.execute(q)
    asins = c.fetchall()

    #testing
    #asins = [("B00VIMMXXG",)]

    for asin in asins:
        print("Scraping " + asin[0])
        raw_data = scrape_amz(asin[0])
        if raw_data != 1:
            q = "create table if not exists " + asin[0] + "_Product_html (retrieved DATETIME, raw_html TEXT)"
            c.execute(q)
            t = (dt.datetime.now(),raw_data[0],)
            q = "insert into " + asin[0] + "_Product_html values (?,?)"
            c.execute(q, t)
            q = "create table if not exists " + asin[0] + "_ProductCart_html (retrieved DATETIME, raw_html TEXT)"
            c.execute(q)
            t = (dt.datetime.now(),raw_data[1],)
            q = "insert into " + asin[0] + "_ProductCart_html values (?,?)"
            c.execute(q, t)
            conn.commit()
        else:
            print("Scrape function returned an error during " + str(asin[0]))
    conn.close()
