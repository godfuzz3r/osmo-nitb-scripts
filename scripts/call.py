#!/usr/bin/env python3
import os
import sys

def call(caller_extension, extension, voice_file):
	if not caller_extension:
		caller_extension = ""
	call_data = """Channel: SIP/GSM/{}
MaxRetries: 10
RetryTime: 10
WaitTime: 30
CallerID: {}
Application: Playback
Data: {}""".format(extension, caller_extension, voice_file)

	call_file = "{}.call".format(extension)
	with open(call_file, "w") as f:
		f.write(call_data)
		f.close()

	os.system("chown asterisk:asterisk {}".format(call_file))
	os.system("mv {} /var/spool/asterisk/outgoing/".format(call_file))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: ./call.py [extention_from] [extention_to] [voice_file]")
        sys.exit(1)

    call(sys.argv[1], sys.argv[2], sys.argv[3])
