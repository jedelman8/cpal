#!/usr/bin/env python
#arista.py 
#Jason Edelman 
#Last Updated 2/18/14

from jsonrpclib import Server
from configobj import ConfigObj
from datetime import datetime

class device1():

	def __init__(self,address,obj):
		self.username = 'arista'
		self.password = 'arista'
		self.address = address	
		self.obj = obj
		self.native = self.jconnect()
		self.facts = self.getFacts()

	def jconnect(self):

		connect_string = "http://" + self.username + ":" + self.password + "@" + self.address + "/command-api"
		#print connect_string
		switch = 'DNE'
		try:
			#print 'Trying to connect...'
			#print 'Using API: ', connect_string
			switch = Server(connect_string)
			#print 'Connection made to ' + self.address + ' successfully.'
		except Exception, e:
			print e
			print 'Unable to connect to device.'

		return switch


	def getPlatform(self,output):
		return output[0]["modelName"]

	def getserialNumber(self,output):
		if output[0]["serialNumber"] == '':
			return '12345'
		else:
			return output[0]["serialNumber"]

	def getUptime(self,response):
		c = response[0]['output']
		return c[:9]
	
	def getHostname(self,output):
		parse = output[0]['output'].split('\n')
		return parse [3].strip()[16:-1]

	def getfreeMemory(self,output):
		return output[0]['memFree']

	def gettotalMemory(self,output):
		return output[0]['memTotal']

	def getFacts(self):
		sh_ver = self.native.runCmds( 1, ["show version"] )
		sh_uptime = self.native.runCmds( 1, ["show uptime"],"text" )
		sh_lldp_localinfo = self.native.runCmds( 1, ["show lldp local-info"],"text")
		#cpu_utilization = self.getCPU(ne)
		free_memory = self.getfreeMemory(sh_ver)
		total_memory = self.gettotalMemory(sh_ver)
		uptime = self.getUptime(sh_uptime)
		platform = self.getPlatform(sh_ver)
		serial_number = self.getserialNumber(sh_ver)
		connect_ip = self.address
		hostname = self.getHostname(sh_lldp_localinfo)

		var_name = self.obj
		
		facts = {'hostname': hostname, 'connect_ip': connect_ip,'platform':platform, 'serial_number':serial_number, 'system_uptime':uptime,'free_system_memory': free_memory, 
			'total_sytem_memory': total_memory,'vendor':'arista','var_name':var_name}

		config = ConfigObj('device_tags.ini').dict()
		for key in config.keys():
			if key == self.address:
				facts.update(config[key])

		return facts

	