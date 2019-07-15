#!/usr/bin/env python
import telnetlib
import sqlite3
import sys
import time

imsi = 999999999999999
HLR_DATABASE = "configs/hlr.sqlite3"

def check_subscriber(imsi):
    conn.write(b"show subscriber imsi %d\n" % imsi)
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for imsi" in res:
        conn.write(b"subscriber create imsi %d\n" % imsi)
        conn.read_until(b"OpenBSC> ")

def get_users():
    # returns user id list generator

    db = sqlite3.connect(HLR_DATABASE)
    c = db.cursor()
    c.execute("SELECT * FROM Subscriber")

    for subscriber in c.fetchall():
        yield subscriber[0]

def ussd_broadcast(type, message):
    users = list(get_users())

    for id in users:
        conn.write(b"subscriber id %d silent-sms sender imsi %d send .SILENT\n" % (id, imsi))
        res = conn.read_until(b"OpenBSC> ")
        if b"%" in res:
            print(res)
            exit(1)

    time.sleep(3)
    for id in users:
        conn.write(b"subscriber id %d ussd-notify %s %s\n" % (id, type, message))
        res = conn.read_until(b"OpenBSC> ")

if __name__ == "__main__":
    try:
        type = int(sys.argv[1])
        message = " ".join(sys.argv[2:])
    except:
        print("usage: ./sms_broadcast.py [ussd-type ( 0|1|2 )] message")
        exit(1)

    conn = telnetlib.Telnet("127.0.0.1", 4242)
    conn.read_until(b"OpenBSC> ")

    check_subscriber(imsi)
    ussd_broadcast(type, message)
