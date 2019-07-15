#!/usr/bin/env python3
import os
import subprocess
import time
import datetime
import signal
from scripts import HLR, user_interact, monitor
import argparse

def signal_handler(sig, frame):
    print('\x1bc')
    stop_services(log=True)
    if os.path.exists("/var/lib/osmocom/hlr.sqlite3"):
        os.remove("/var/lib/osmocom/hlr.sqlite3")

    #print("\x1b[2J")
    print("Exiting...")
    time.sleep(2)
    exit(0)


def check_root():
    if not os.geteuid() == 0:
        print("Run as root!")
        return False
    else:
        return True


def sdr_check():
    print("[*] Checking for SDR device..")
    p = subprocess.Popen(['LimeUtil', '--find'], stdout=subprocess.PIPE)
    output, err = p.communicate()
    rc = p.returncode

    if b"LimeSDR" in output:
        print("[+] Found device: " + output.decode())
    else:
        print("[-] Not devices found, exiting...")
        exit(1)


#configure osmocom, systemctl and asterisk
def configure(gprs, sip, interface, config_path="/etc/osmocom"):
    # stopping osmocom services, if they a running
    stop_services()

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    app_dir = os.path.dirname(os.path.realpath(__file__))

    if gprs:
        subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/openbsc_egprs.cfg", config_path+"/osmo-nitb.cfg"), shell=True)
        subprocess.call("su -c \"echo \'1\' > /proc/sys/net/ipv4/ip_forward\"", shell=True)
        subprocess.call("iptables -A POSTROUTING -s 176.16.1.1/24 -t nat -o {} -j MASQUERADE".format(interface), shell=True)
    else:
        subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/openbsc.cfg", config_path+"/osmo-nitb.cfg"), shell=True)


    subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-pcu.cfg", config_path+"/osmo-pcu.cfg"), shell=True)
    subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-sgsn.cfg", config_path+"/osmo-sgsn.cfg"), shell=True)
    subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-ggsn.cfg", config_path+"/osmo-ggsn.cfg"), shell=True)

    subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-bts.cfg", config_path+"/osmo-bts-trx.cfg"), shell=True)
    subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-trx.cfg", config_path+"/osmo-trx-lms.cfg"), shell=True)

    if sip:
        subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/osmo-sip-connector.cfg", config_path+"/osmo-sip-connector.cfg"), shell=True)
        subprocess.call("cp -f {0} {1}".format(app_dir+"/services/osmo-nitb_sip.service", "/lib/systemd/system/osmo-nitb.service"), shell=True)
        subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/extensions.conf", "/etc/asterisk/extensions.conf"), shell=True)
        subprocess.call("cp -f {0} {1}".format(app_dir+"/configs/sip.conf", "/etc/asterisk/sip.conf"), shell=True)
    else:
        subprocess.call("cp -f {0} {1}".format(app_dir+"/services/osmo-nitb.service", "/lib/systemd/system/osmo-nitb.service"), shell=True)

    subprocess.call("sysctl -w kernel.sched_rt_runtime_us=-1", shell=True)
    subprocess.call("systemctl daemon-reload", shell=True)


def run(gprs, sip):
    services = ["osmo-nitb.service", "osmo-trx-lms.service", "osmo-bts-trx.service"]
    if gprs:
        services += ["osmo-pcu.service", "osmo-ggsn.service", "osmo-sgsn.service"]
    if sip:
        services += ["osmo-sip-connector", "asterisk"]

    for service in services:
        print("[+] starting {0} ...".format(service))
        subprocess.call("systemctl start {0}".format(service), shell=True)

        check_errors(service=service)


def stop_services(log=False):
    services = ["osmocom-nitb.service",
                "osmo-nitb.service",
                "osmo-trx-lms.service",
                "osmo-bts-trx.service",
                "osmo-pcu.service",
                "osmo-ggsn.service",
                "osmo-sgsn.service",
                "osmo-sip-connector",
                "asterisk"]

    for service in services:
        p = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
        output, err = p.communicate()

        if b"Active: active" in output or b"activating (auto-restart)" in output:
            if log:
                print("[*] Stopping {0} ...".format(service))

            subprocess.call(["systemctl", "stop", service])


def check_errors(gprs=False, sip=False, service=False):
    if not service:
        services = ["osmo-nitb.service", "osmo-trx-lms.service", "osmo-bts-trx.service"]
        if gprs:
            services += ["osmo-pcu.service", "osmo-ggsn.service", "osmo-sgsn.service"]
        if sip:
            services += ["osmo-sip-connector"]
    else:
        services = [service]

    date = datetime.datetime.now()

    for service in services:
        #s = subprocess.Popen(["journalctl", "-b", "-S",
        #                         "{0}:{1}:{2}".format(date.hour, date.minute, date.second),
        #                         "-u", service], stdout=subprocess.PIPE).communicate()[0]

        #print(s.decode())
        #if b"Failed with result 'exit-code'" in s:
        status = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE).communicate()[0]
        if not b"active (running)" in status:
            print( "Somethigs wrong with {0}, see journalctl -b -S {1} -u {0}".format(
                    service,
                   "{0}:{1}:{2}".format(date.hour, date.minute, date.second))
                  )
            stop_services()
            exit(1)


help_message = """
Script for automaticaly preparing and deploying Osmocom GSM stack.

"""

if __name__ == "__main__" and check_root():
    parser = argparse.ArgumentParser(description=help_message)

    parser.add_argument("-u", "--interact",
                         action="store_true", dest="user_interaction", default=False,
                         help="Enable automaticaly interaction with all new users.")

    parser.add_argument("-c", default="config.json", dest="config",
                        help="Config file for auto user interaction. (Default=config.json)")

    parser.add_argument("--gprs", action="store_true", default=False,
                        help="Enable E(GPRS) support. (Default=False)")

    parser.add_argument("-i", default="wlan0", dest="interface",
                        help="Interface to routing E(GPRS). (Default=wlan0)")

    parser.add_argument("--sip", action="store_true", default=False,
                        help="Enable sip (Asterisk) support. (Default=False)")

    args = parser.parse_args()

    hlr_path = "/var/lib/osmocom/hlr.sqlite3"
    user_interaction = args.user_interaction
    config = args.config
    gprs = args.gprs
    interface = args.interface
    sip = args.sip

    signal.signal(signal.SIGINT, signal_handler)

    sdr_check()
    configure(gprs, sip, interface)

    run(gprs, sip)
    check_errors()
    db = HLR.Database(hlr_path)
    print("[+] Done")
    time.sleep(3)

    while 1:
        for user in db.get_new_users():
            extension = user[5]
            time.sleep(3)
            user_interact.interact(config, extension)

        monitor.update_monitor(db.get_subscribers())
        check_errors()
        time.sleep(1)
