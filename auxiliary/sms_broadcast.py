#!/usr/bin/env python
import telnetlib
import sqlite3
import sys

imsi = 999999999999999
HLR_DATABASE = "configs/hlr.sqlite3"

def check_extension(extension):
    conn.write(b"show subscriber extension %s\n" % extension)
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for extension" in res:
        create_subscriber(extension)

def create_subscriber(extension):
    print("No user with excension %s found. Creating new..." % extension)
    print("Extension: %s, IMSI: %d" % (extension, imsi))

    conn.write(b"show subscriber imsi %d\n" % imsi)
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for imsi" in res:
        conn.write(b"subscriber create imsi %d\n" % imsi)
        conn.read_until(b"OpenBSC> ")

    conn.write(b"enable\n")
    conn.read_until(b"OpenBSC# ")
    conn.write(b"subscriber imsi %d extension %s\n" % (imsi, extension))
    conn.read_until(b"OpenBSC# ")
    conn.write(b"disable\n")
    conn.read_until(b"OpenBSC> ")

def get_users():
    # returns user id list generator

    db = sqlite3.connect(HLR_DATABASE)
    c = db.cursor()
    c.execute("SELECT * FROM Subscriber")

    for subscriber in c.fetchall():
        yield subscriber[0]

def send_sms(id, extension, message):
    conn.write(b"subscriber id %d sms sender extension %s send %s\n" % (id, extension, message))
    res = conn.read_until(b"OpenBSC> ")
    if b"%" in res:
        print(res)
        exit(1)

if __name__ == "__main__":
    try:
        extension = sys.argv[1]
        message = " ".join(sys.argv[2:])
    except:
        print("usage: ./sms_broadcast.py extension message")
        exit(1)

    conn = telnetlib.Telnet("127.0.0.1", 4242)
    conn.read_until(b"OpenBSC> ")

    check_extension(extension)

    for id in get_users():
        send_sms(id, extension, message)
