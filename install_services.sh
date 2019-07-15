#!/bin/sh
cp services/osmo-nitb.service /lib/systemd/system
cp services/osmo-bts-trx.service /lib/systemd/system
cp services/osmo-trx-lms.service /lib/systemd/system
cp services/osmo-pcu.service /lib/systemd/system
cp services/osmo-sgsn.service /lib/systemd/system
cp services/osmo-ggsn.service /lib/systemd/system
cp services/osmo-sip-connector.service /lib/systemd/system

systemctl daemon-reload