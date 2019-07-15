#!/usr/bin/env python3
import telnetlib
import sqlite3
import sys
import time

imsi = 999999999999999

def check_subscriber(imsi, conn):
    conn.write("show subscriber imsi {}\n".format(imsi).encode())
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for imsi" in res:
        conn.write("subscriber create imsi {}\n".format(imsi).encode())
        conn.read_until(b"OpenBSC> ")

def send(extension, type, message):
    conn = telnetlib.Telnet("127.0.0.1", 4242)
    conn.read_until(b"OpenBSC> ")

    check_subscriber(imsi, conn)

    conn.write("subscriber extension {} silent-sms sender imsi {} send .SILENT\n".format(extension, imsi).encode())
    res = conn.read_until(b"OpenBSC> ")
    if b"%" in res:
        print(res)
        return False

    time.sleep(3)
    conn.write("subscriber extension {} ussd-notify {} {}\n".format(extension, type, message).encode())
    res = conn.read_until(b"OpenBSC> ")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: ./sms.py [extension] [ussd-type] [\"message\"]")
        sys.exit(1)

    extension = sys.argv[1]
    ussd_type = sys.argv[2]
    message = sys.argv[3]
    send(extension, ussd_type, message)