#!/usr/bin/env python
'''
This is the main module of the common programmable abstraction layer.  It
returns a data structure of type 'device.'  Ultimately, it is passing back
the native device type of said vendor API.  For example, it returns a NE for
Cisco onePK and returns the main device for Arista eAPI (switch = Server(connection_parameters)).
It's basically returning 'switch.'  __init__ calls the right vendor API and
gathers device facts.  It is also returns a global list of connected_devices.
'''

import json
import random
import sys
import atexit
from datetime import datetime
from cpal.core.counter import counter
import pandums
import pprint
from cpal.vendors.arista.apis.eapi.eapi import arista
from cpal.vendors.cisco.apis.onepk.onepk import cisco
from cpal.vendors.f5.apis.icontrol.icontrol import f5

import argparse


__author__ = "Jason Edelman and ...come help out!"
__copyright__ = "Copyright 2014, The CPAL Project"
__version__ = "1.0.0"
__maintainer__ = "Jason Edelman"
__email__ = "jedelman8@gmail.com"
__status__ = "Development"

tracker = counter()


class device():
    def __init__(self, obj='', manufacturer='', address=''):
        self.facts_expanded = {}
        self._thisdevice = ''
        self.native = ''
        self.connected_devices = []
        self.facts = {}

        # initialize variables with command-line arguments
        # added switches to allow script type use, such as -i [ip-address]
        parser = argparse.ArgumentParser(description='\
            input -f [function] -i [ip_address] \
            -u [username] -p [password] -m [manufacturer]'\
            )

        parser.add_argument('-f', '--function', help='i.e. -f IntfStatus, show version')
        parser.add_argument('-c', '--cli', help='i.e. same as -f, for redundancy')
        parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
        parser.add_argument('-u', '--username', help='Enter username of device')
        parser.add_argument('-p', '--password', help='Enter password for username')
        parser.add_argument('-m', '--manufacturer', help='Set the manufacturer to make calls on')
        parser.add_argument('-n', '--name', help='Sets the var_name')
        arg = parser.parse_args()

        # set ip address to make calls on
        if arg.ip_address:
            self.address = arg.ip_address
        else:
            self.address = address

        # set manufacturer based on input
        if arg.manufacturer:
            self.manufacturer = arg.manufacturer
        else:
            self.manufacturer = manufacturer

        # set var_name or obj as already named
        if arg.name:
            self.obj = arg.name
        else:
            self.obj = obj

        self.deviceCalls(self.obj)

    # makes actual calls once internal variables are initialized
    # this method was moved from outside of __init__ to make it more modular
    def deviceCalls(self, obj):
        if self.manufacturer.lower() == 'cisco':
            self._thisdevice = cisco(self.address, obj)
            self.native = self._thisdevice.native
            if self.native != 'DNE':
                self.facts = self._thisdevice.getFacts()
                #self.facts_expanded = self._thisdevice.getFacts_expanded()
        elif self.manufacturer.lower() == 'arista':
            self._thisdevice = arista(self.address, obj)
            self.native = self._thisdevice.native
        #if self.native != 'DNE':
            #print self.native
            self.facts = self._thisdevice.getFacts()
      	elif manufacturer.lower() == 'f5':
			self._thisdevice = f5(self.address,obj)
			self.native = self._thisdevice.native
			self.facts = self._thisdevice.getFacts()

		self.connected_devices = tracker.calc(obj,self.address,self.facts['hostname'])
          



    def refreshFacts(self):
        self.facts = self._thisdevice.getFacts()
        print 'Refreshed'

    def getFacts_expanded(self):
        self.facts_expanded = self._thisdevice.getFacts_expanded()

<<<<<<< HEAD
    def getserialNumber(self):
        return self._thisdevice.getserialNumber()
=======
	def getCPU(self):
		return self._thisdevice.getCPU()
		
	def getVersion(self):
		return self._thisdevice.getVersion()

        def getBaseMAC(self):
		return self._thisdevice.getBaseMAC()
>>>>>>> 5974cab8b67e5eeed4a4cb1d1b62f2436617de84

    def getCPU(self):
        return self._thisdevice.getCPU()

    def getfreeMemory(self):
        return self._thisdevice.getfreeMemory()

    def gettotalMemory(self):
        return self._thisdevice.gettotalMemory()

<<<<<<< HEAD
    def getHostname(self):
        return self._thisdevice.getHostname()
=======
	def getTime(self):
		return self._thisdevice.getTime()

	def getTimeZone(self):
		return self._thisdevice.getTimeZone()

	def getUptime(self):
		return self._thisdevice.getUptime()
		
	def getPlatform(self):
		return self._thisdevice.getPlatform()
>>>>>>> 5974cab8b67e5eeed4a4cb1d1b62f2436617de84

    def getUptime(self):
        return self._thisdevice.getUptime()

    def getPlatform(self):
        return self._thisdevice.getPlatform()

    def getReasonforReboot(self):
        return self._thisdevice.getReasonforReboot()

    def getInterfaces(self):
        return self._thisdevice.getInterfaces()

    def getInterfaceDetail(self):
        return self._thisdevice.getInterfaceDetail()

<<<<<<< HEAD
    def cli(self, command):
        return self._thisdevice.useCLI(command)

    def getRoutes(self):
        return self._thisdevice.getRoutes()
=======
	#def disconnect(self):
	#	self.native.disconnect()
	#	print 'Disconnected'
>>>>>>> 5974cab8b67e5eeed4a4cb1d1b62f2436617de84

    #def disconnect(self):
    #   self.native.disconnect()
    #   print 'Disconnected'


'''if __name__ == "__main__":

<<<<<<< HEAD
    # Yandy for testing, values can be passed into __init__
    # dev1 = device("dev1", "arista", "192.168.31.22")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dev1.facts)

    # Yandy for testing, values can be as command-line arguments 
    # comment above section and add -- python main.py -i [ip_address] -m [manufacturer] -n 'SW1'
    dev1 = device()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(dev1.facts)

    # --------------------------------------------------------

    # --------------------------------------------------------
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print 'Connecting to device...'
    # r2 = device('cisco','10.1.1.120')
    # print 'Connected to device1!'
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print 'Connecting to next device...'
    # r3 = device('cisco','10.1.1.130')
    # print 'Connected to device2'
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # devlist = [r2,r3]
    # row = []
    # for dev in devlist:
    #     temp = []
    #     temp.append(dev.facts['hostname'])
    #     temp.append(dev.facts['serial_number'])
    #     temp.append(dev.facts['last_reboot_reason'])
    #     row.append(temp)
    # headers = [['Hostname', 'Serial Number', 'Last Reboot Reason']]
    # table = headers + row
    # print 'almost there...'
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # pandums.pprint_table(table)
    # sys.exit()
    # --------------------------------------------------------
=======
	r1 = device("r1","cisco","10.1.1.110")
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print 'Connecting to device...'
	r2 = device('cisco','10.1.1.120')
	print 'Connected to device1!'
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print 'Connecting to next device...'
	r3 = device('cisco','10.1.1.130')
	print 'Connected to device2'
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	devlist = [r2,r3]
	row = []
	for dev in devlist:
		temp = []
		temp.append(dev.facts['hostname'])
		temp.append(dev.facts['serial_number'])
		temp.append(dev.facts['last_reboot_reason'])
		row.append(temp)
	headers = [['Hostname', 'Serial Number', 'Last Reboot Reason']]
	table = headers + row
	print 'almost there...'
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	pandums.pprint_table(table)
	sys.exit()'''
>>>>>>> 5974cab8b67e5eeed4a4cb1d1b62f2436617de84
