
![](https://raw.githubusercontent.com/DrLafa/osmo-nitb-scripts/master/doc/img/help.png)

### RougeBTS

 This project is created for easy deployment of Osmocom GSM stack and convenient interaction with users

  - E(GPRS) support
  - Asterisk support
  - monitoring online subscribers
  - automatic interaction with new users, like sms, ussd or call
  - manual interaction with individual users
  - USSD-broadcast
  - SMS-broadcast
  - SMS-spam ;)


![](https://raw.githubusercontent.com/DrLafa/osmo-nitb-scripts/master/doc/img/RougeBTS.png)

All software was tested on [LimeSDR-Mini + Orange Pi Zero](https://codeby.net/threads/miniatjurnaja-sotovaja-stancija-na-baze-limesdr-mini-i-orange-pi-zero.66747/) with Armbian Bionic. Also with Debian 10

### Installation
Installing LimeSuite
```
apt install git g++ cmake libsqlite3-dev libi2c-dev libusb-1.0-0-dev
git clone https://github.com/myriadrf/LimeSuite.git
cd LimeSuite
mkdir builddir && cd builddir
cmake ../
make -j4
sudo make install
sudo ldconfig
cd ../udev-rules/
sudo sh LimeSuite/udev-rules/install.sh
cd ~/
```
Adding the Osmocom repository
```
sudo su
wget http://download.opensuse.org/repositories/network:/osmocom:/latest/Debian_10//Release.key
apt-key add Release.key
rm Release.key
echo "deb  http://download.opensuse.org/repositories/network:/osmocom:/latest/Debian_10/ ./" > /etc/apt/sources.list.d/osmocom-latest.list
apt update
exit
```
Installing
```
sudo apt install osmocom-nitb osmo-trx-lms osmo-bts-trx osmo-ggsn osmo-sgsn osmo-pcu osmo-sip-connector libsofia-sip-ua-glib-dev asterisk sqlite3 libsmpp1 telnet python3-pip
sudo pip3 install smpplib
```
It is necessary to install Osmocom stack from apt, because it configure Systemd services. If you compile osmocom from sources, you need to install Systemd services by yourself with script `install_services.sh`
```
sudo ./install_services.sh
```
Stopping launched services after installation
```
sudo su
systemctl stop osmocom-nitb
systemctl stop osmo-nitb
systemctl stop osmo-trx-lms
systemctl stop osmo-bts-trx
systemctl stop osmo-ggsn
systemctl stop osmo-sgsn
systemctl stop osmo-pcu
systemctl stop osmo-sip-connector
systemctl stop asterisk
exit
```
Disabling service autostart
```
sudo su
systemctl disable osmocom-nitb
systemctl disable osmo-nitb
systemctl disable osmo-trx-lms
systemctl disable osmo-bts-trx
systemctl disable osmo-ggsn
systemctl disable osmo-sgsn
systemctl disable osmo-pcu
systemctl disable osmo-sip-connector
systemctl disable asterisk
```
Cloning
```
git clone https://github.com/DrLafa/osmo-nitb-scripts
```

### Configure
All osmocom config files stored in `config/` folder and updating everytime when you start `main.py`. You can change it by youself.

### config.json
For easy setup of user-interactivity you can use config.json
- config.json example
```
{
   "scripts":{
      "sms":{
         "enabled": false,
         "sender_extension": "John Connor",
         "message":[
            "If you are reading this, then you are resistance"
         ]
      },
      "ussd":{
         "enabled": false,
         "ussd_type": 1,
         "message":[
            "Welcome to our l33t hax0r network.",
            "If you are reading this, then you are true L33T 1337 H4xXx0r"
         ]
      },
      "call":{
         "enabled": true,
         "caller_extension": 666,
         "voice-file": "tt-monkeys"
      }
   }
}
```
#### sms
Send sms to new users. When user connect to network, script choose 1 random message from ```message``` section and sending it from extension ```sender_extension```

#### ussd
Send ussd to new users. Script choose 1 random message from ```message``` section adn sending it to user

#### call
Make a call to new user. This function works only with Asterisk support. voice-file is 16-bit 8 kHz wav file. If ```caller_extension``` is ```false```, then the user sees that the phone is not defined.
