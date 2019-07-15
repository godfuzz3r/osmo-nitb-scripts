#!/usr/bin/env python
import telnetlib
import sys
import random
import time

imsi = 999999999999999

def check_extension(extension):
    conn.write(b"show subscriber extension %s\n" % extension)
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for extension" in res:
        print("Phone with extension %s not found ;(" % extension)
        exit(1)

def check_spam_subscriber():
    conn.write(b"show subscriber imsi %d\n" % imsi)
    res = conn.read_until(b"OpenBSC> ")

    if b"No subscriber found for imsi" in res:
        conn.write(b"subscriber create imsi %d\n" % imsi)
        print(conn.read_until(b"OpenBSC> "))

def send(extension, spam_number, message):
    print("Sending sms from %d..." % spam_number)

    conn.write(b"enable\n")
    conn.read_until(b"OpenBSC# ")
    conn.write(b"subscriber imsi %d extension %d\n" % (imsi, spam_number))
    conn.read_until(b"OpenBSC# ")
    conn.write(b"disable\n")
    conn.read_until(b"OpenBSC> ")

    conn.write(b"subscriber extension %s sms sender extension %d send %s\n" % (extension, spam_number, message))
    res = conn.read_until(b"OpenBSC> ")

    if b"%" in res:
        print(res)
        exit(1)

if __name__ == "__main__":
    try:
        extension = sys.argv[1]
        repeats = int(sys.argv[2])
        message = " ".join(sys.argv[3:])
    except:
        print("usage: ./sms_broadcast.py extension [num of repeats] message")
        exit(1)

    conn = telnetlib.Telnet("127.0.0.1", 4242)
    conn.read_until(b"OpenBSC> ")

    check_extension(extension)
    check_spam_subscriber()

    for _ in range(repeats):
        spam_number = random.randint(1000,9999)
        send(extension, spam_number, message)
        time.sleep(2)
