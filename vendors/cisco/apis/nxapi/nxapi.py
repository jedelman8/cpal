#!/usr/bin/env python

'''

This is the Cisco NXAPI module for CPAL. At the moment, it requires Matt Oswalt's fork of the nexus9000 repository:
https://github.com/Mierdin/nexus9000
(This is because Cisco's fork is not offered as an installable module, yet. I am currently working through this with Cisco and will update this documentation when their repo has this option)

This module will address functionality offered by NXAPI on the Nexus 9000 platform in standalone mode. A separate module
will be developed for interation with the APIC when information becomes available.

Author: Matt Oswalt
Email: matt@keepingitclassless.net

'''

from nxos.nxapi.utils.nxapi_utils import *
from collections import OrderedDict
from array import *

class cpalNexus9000():
		
		def __init__(self, url, username, password):
			self.url = 'http://10.2.1.8/ins'
			self.username = 'admin'
			self.password = 'Cisco.com'
			#Add more properties/facts here

		def sendCmd(self, msgtype, command):
			thisNXAPI = NXAPI()
			thisNXAPI.set_target_url(self.url)
			thisNXAPI.set_username(self.username)
			thisNXAPI.set_password(self.password)
			thisNXAPI.set_msg_type(msgtype)
			thisNXAPI.set_cmd(command)
			return thisNXAPI.send_req()

		def getserialNumber(self):
			return xmltodict.parse(self.sendCmd('cli_show', 'show license host-id')[1])['ins_api']['outputs']['output']['body']['host_id']

		def getCPU(self):
			#This output is not optimal, due to NXAPI limitations
			return xmltodict.parse(self.sendCmd('cli_show_ascii', 'show proc cpu | i "CPU util"')[1])['ins_api']['outputs']['output']['body']['hostname']

		def getfreeMemory(self):
			return null

		def gettotalMemory(self):
			return xmltodict.parse(self.sendCmd('cli_show', 'show hostname')[1])['ins_api']['outputs']['output']['body']['memory'] #Provided in kB

		def getHostname(self):
			return xmltodict.parse(self.sendCmd('cli_show', 'show version')[1])['ins_api']['outputs']['output']['body']['hostname']

		def getUptime(self):
			#This output is not optimal, due to NXAPI limitations
			return xmltodict.parse(self.sendCmd('cli_show_ascii', 'show system uptime | i "System uptime"')[1])['ins_api']['outputs']['output']['body']['hostname']
		
		def getPlatform(self):
			return xmltodict.parse(self.sendCmd('cli_show', 'show version')[1])['ins_api']['outputs']['output']['body']['chassis_id']

		def getReasonforReboot(self):
			return xmltodict.parse(self.sendCmd('cli_show', 'show version')[1])['ins_api']['outputs']['output']['body']['rr_reason']

		def getInterfaces(self):
			return null

		def getInterfaceDetail(self):
			return null

		def addCDPListener(self):
			return null

		def getNeighbors(self):
			return null

		def getRoutes(self):
			return null

		#need to have a "load" module that pulls properties upon class instantiation
		# def getFacts(self):
		# 	cpu_utilization = self.getCPU()
		# 	free_memory = self.getfreeMemory()
		# 	total_memory = self.gettotalMemory()
		# 	hostname = self.getHostname()
		# 	uptime = self.getUptime()
		# 	platform = self.getPlatform()
		# 	serial_number = self.getserialNumber()
		# 	reboot_reason = self.getReasonforReboot()
		# 	connect_ip = self.address
		# 	interfaces = self.getInterfaces()
			
			
		# 	facts = {'connect_ip': connect_ip,'serial_number': serial_number, 'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory, 
		# 			'total_sytem_memory': total_memory,'hostname': hostname, 'system_uptime': uptime, 'platform': platform,
		# 			'last_reboot_reason': reboot_reason, 'vendor':'cisco','interfaces':interfaces,'var_name':self.obj}

		# 	config = ConfigObj('device_tags.ini').dict()
		# 	for key in config.keys():
		# 		if key == self.address:
		# 			facts.update(config[key])
		# 	return facts

		# def getFacts_expanded(self):
		# 	neighbors = self.getNeighbors()
		# 	interface_detail = self.getInterfaceDetail()
		# 	facts = {'neighbors':neighbors,'interface_detail':interface_detail}
		# 	facts.update(self.getFacts())

		# 	return facts

thisNexus = cpalNexus9000('http://10.2.1.8/ins','admin','Cisco.com')
print thisNexus.getserialNumber()