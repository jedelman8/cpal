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
from counter import counter
import pandums
#from cpal.vendors.arista.apis.eapi.eapi import arista
#from cpal.vendors.cisco.apis.onepk.onepk import cisco
from cpal.vendors.f5.apis.icontrol.icontrol import f5

__author__ = "Jason Edelman and ...come help out!"
__copyright__ = "Copyright 2014, The CPAL Project"
__version__ = "1.0.0"
__maintainer__ = "Jason Edelman"
__email__ = "jedelman8@gmail.com"
__status__ = "Development"

tracker = counter()

class device():	

	def __init__(self, obj, manufacturer, address):
		self.manufacturer = manufacturer
		self.address = address
		if self.manufacturer.lower() == 'cisco':
			self._thisdevice = cisco(self.address,obj)
			self.native = self._thisdevice.native
			if self.native != 'DNE':
				self.facts = self._thisdevice.getFacts()				
				#self.facts_expanded = self._thisdevice.getFacts_expanded()
			
		elif manufacturer.lower() == 'arista':
			self._thisdevice = arista(self.address,obj)
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

		self.facts_expanded =  self._thisdevice.getFacts_expanded()

	def getserialNumber(self):
		return self._thisdevice.getserialNumber()

	def getCPU(self):
		return self._thisdevice.getCPU()

	def getfreeMemory(self):
		return self._thisdevice.getfreeMemory()

	def gettotalMemory(self):
		return self._thisdevice.gettotalMemory()

	def getHostname(self):
		return self._thisdevice.getHostname()

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

	def cli(self,command):
		return self._thisdevice.useCLI(command)

	def getRoutes(self):
		return self._thisdevice.getRoutes()

	def getPools(self):
		return self._thisdevice.getPools()

	#def disconnect(self):
	#	self.native.disconnect()
	#	print 'Disconnected'


	#atexit.register(disconnect) #currently not working
	

if __name__ == "__main__":

	r1 = device("r1","cisco","10.1.1.110")
	'''print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
