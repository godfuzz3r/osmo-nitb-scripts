#!/usr/bin/env python3
from scripts import HLR, user_interact, monitor
import argparse

help_message = """
Script for interaction with users

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument("-c", "--config", default="config.json",
                        help="Config file for auto user interaction. (Default=config.json)")

    parser.add_argument("-D", "--hlr", default="/var/lib/osmocom/hlr.sqlite3",
                        help="Config file for auto user interaction. (Default=/var/lib/osmocom/hlr.sqlite3)")

    parser.add_argument("-e", "--extension", default="all",
                        help="Phone number. (Default=all)")


    args = parser.parse_args()
    if args.extension == "all":
        try:
            db = HLR.Database(args.hlr)
            for user in db.get_subscribers():
                extension = user[5]
                user_interact.interact(args.config, extension)
                monitor.update_monitor(db.subscribers)

        except Exception as e:
            print("[-] {}".format(e))
            exit(1)
    else:
        user_interact.interact(args.config, args.extension)
