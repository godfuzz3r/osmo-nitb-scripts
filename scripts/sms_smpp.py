#!/usr/bin/env python3
# -*- encoding: UTF-8 -*-
import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

logging.basicConfig(level = logging.DEBUG,
	format = "%(levelname)s %(filename)s:%(lineno)d %(message)s")

def send_message(source, dest, string):
	client = smpplib.client.Client('127.0.0.1', 2775)

	# Print when obtain message_id
	client.set_message_sent_handler(
		lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
	client.set_message_received_handler(
		lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

	client.connect()
	client.bind_transceiver(system_id='OSMO-SMPP', password='1234')

	parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(string)
	#part = b"".join(parts)

	try:
		string.encode("ascii")
		coding = encoding_flag
	except:
		coding = smpplib.consts.SMPP_ENCODING_ISO10646
		
	logging.info('Sending SMS "%s" to %s' % (string, dest))
	for part in parts:
		pdu = client.send_message(
			msg_type=smpplib.consts.SMPP_MSGTYPE_USERACK,
			source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
			source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
			source_addr=source,
			dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
			dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
			destination_addr=dest,
			short_message=part,
			data_coding=coding,
			esm_class=msg_type_flag,
			#esm_class=smpplib.consts.SMPP_MSGMODE_FORWARD,
			registered_delivery=True,
		)
		#print(pdu.generate())
	logging.debug(pdu.sequence)


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("usage: ./sms.py [from] [to] [\"message\"]")
		sys.exit(1)

	source = sys.argv[1]
	dest = sys.argv[2]
	message = sys.argv[3]

	send_message(source, dest, message)