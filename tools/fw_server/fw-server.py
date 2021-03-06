#!/usr/bin/env python3

"""
  fw-server.py - firmware server for Sonoff-Tasmota OTA upgrade

  Copyright (C) 2018 Gennaro Tortone

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
   - Python3
   - pip install netifaces flask

Instructions:
    Copy Sonoff-Tasmota firmware binary files in 'fw' directory.
    A set of prebuilt files can be downloaded by Sonoff-Tasmota release page:
        https://github.com/arendst/Sonoff-Tasmota/releases

    Configure your Sonoff-Tasmota device with your fw-server URL:
        Firmware Upgrade -> Upgrade by web server
            http://<ip_address>:5000/sonoff-minimal.bin

Usage:
   ./fw-server.py -d <net_iface>   (default: eth0)
		or
	./fw-server.py -i <ip_address>

Example:
	./fw-server.py -d wlan0
		or
	./fw-server.py -i 192.168.1.10
"""

import io
import os.path
from sys import exit
from flask import Flask, send_file
from optparse import OptionParser
import netifaces as ni


usage = "usage: fw-server {-d | -i} arg"
parser = OptionParser(usage)
parser.add_option("-d", "--dev", action="store", type="string",
                  dest="netdev", default="eth0", help="network interface (default: eth0)")
parser.add_option("-i", "--ip", action="store", type="string",
                  dest="ip", help="IP address to bind")
(options, args) = parser.parse_args()

if options.ip is None:
	try:
		netip = ni.ifaddresses(options.netdev)[ni.AF_INET][0]['addr']
	except Exception as e:
		print("E: network interface error - {}".format(e))
		exit(1)
else:
	netip = options.ip

app = Flask(__name__)

@app.route('/<filename>')
def fw(filename):
   if(os.path.exists("fw/" + str(filename))):
      return send_file("fw/" + str(filename), attachment_filename=filename, mimetype='application/octet-stream')
   else:
      return("ERROR: file not found")

if __name__ == "__main__":
    try:
        app.run(host=netip)
    except Exception as e:
        print("E: {}".format(e))
