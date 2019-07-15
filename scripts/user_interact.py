#!/usr/bin/env python3
import json
import random
from scripts import sms_smpp, ussd, call
import sys

def interact(config, extension):
	print("executing script...")

	with open(config, encoding="utf-8") as data:
		config = json.load(data)["scripts"]

	if config["sms"]["enabled"]:
		sender_extension = config["sms"]["sender_extension"]
		message = random.choice(config["sms"]["message"])

		sms_smpp.send_message(sender_extension, str(extension), message)

	if config["ussd"]["enabled"]:
		ussd_type = int(config["ussd"]["ussd_type"])
		message = random.choice(config["ussd"]["message"])

		ussd.send(extension, ussd_type, message)

	if config["call"]["enabled"]:
		caller_extension = config["call"]["caller_extension"]
		voice_file = config["call"]["voice-file"]

		call.call(caller_extension, extension, voice_file)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("usage: python3 user_interact.py [extension]")
		exit(1)

	interact(int(sys.argv[1]))
