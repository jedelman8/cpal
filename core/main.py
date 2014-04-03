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
import argparse
from cpal.vendors.arista.apis.eapi.eapi import arista
from cpal.vendors.cisco.apis.onepk.onepk import cisco
from cpal.vendors.f5.apis.icontrol.icontrol import f5



__author__ = "Jason Edelman"
__copyright__ = "Copyright 2014, The CPAL Project"
__version__ = "1.0.0"
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
        self.manufacturer = manufacturer
        self.obj = obj
        self.address = address

        self.deviceCalls()


    # makes actual calls once internal variables are initialized
    # this method was moved from outside of __init__ to make it more modular
    def deviceCalls(self):
        if self.manufacturer.lower() == 'cisco':
            self._thisdevice = cisco(self.address, self.obj)
            self.native = self._thisdevice.native
            if self.native != 'DNE':
                self.facts = self._thisdevice.getFacts()
                #self.facts_expanded = self._thisdevice.getFacts_expanded()
        elif self.manufacturer.lower() == 'arista':
            self._thisdevice = arista(self.address, self.obj)
            self.native = self._thisdevice.native
            #if self.native != 'DNE':
                #print self.native
            #self.facts = self.getFacts()
      	elif self.manufacturer.lower() == 'f5':
			self._thisdevice = f5(self.address,self.obj)
			self.native = self._thisdevice.native
			self.facts = self._thisdevice.getFacts()

        #self.connected_devices = tracker.calc(self.obj,self.address,self.facts['hostname'])

    # Yandy: added getFacts to device, to streamline the calling a bit.
    # can easily be taken off, if not desired.
    def getFacts(self):
        self.facts = self._thisdevice.getFacts()
        return self.facts

    def refreshFacts(self):
        self.facts = self._thisdevice.getFacts()
        print 'Refreshed'

    def getFacts_expanded(self):
        self.facts_expanded = self._thisdevice.getFacts_expanded()


    def getserialNumber(self):
        return self._thisdevice.getserialNumber()

	def getCPU(self):
		return self._thisdevice.getCPU()
		
	def getVersion(self):
		return self._thisdevice.getVersion()

    def getBaseMAC(self):
		return self._thisdevice.getBaseMAC()


    def getCPU(self):
        return self._thisdevice.getCPU()

    def getfreeMemory(self):
        return self._thisdevice.getfreeMemory()

    def gettotalMemory(self):
        return self._thisdevice.gettotalMemory()


    def getHostname(self):
        return self._thisdevice.getHostname()

	def getTime(self):
		return self._thisdevice.getTime()

	def getTimeZone(self):
		return self._thisdevice.getTimeZone()

	def getUptime(self):
		return self._thisdevice.getUptime()
		
	def getPlatform(self):
		return self._thisdevice.getPlatform()


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


    def cli(self, command):
        return self._thisdevice.useCLI(command)

    def getRoutes(self):
        return self._thisdevice.getRoutes()

	def d(self):
		self._thisdevice.disconnect()
		print 'Disconnected'


def createDevice(args):
    dev = device('dev',args['manufacturer'],args['ip_address'])
    #print dev.getserialNumber()
    function = args['function']
    value = getattr(dev, function)()

    # prettifies the printing a bit, in case the returned value is more complex than a string
    if type(value) is dict:
    	pp = pprint.PrettyPrinter(indent=4)
    	pp.pprint(value)
    else:
    	print value
    
    if args['manufacturer'] == 'cisco':
        dev.native.disconnect()

    
if __name__ == "__main__":

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

    args = vars(parser.parse_args())
    
    createDevice(args)
    # Yandy for testing, values can be passed into __init__
    # dev1 = device("dev1", "arista", "192.168.31.22")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dev1.facts)

    # Yandy for testing, values can be as command-line arguments 
    # comment above section and add -- python main.py -i [ip_address] -m [manufacturer] -f [function]
 