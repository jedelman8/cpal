#!/usr/bin/env python

'''
This is the F5 Networks BIG-IP iControl (SOAP) module for CPAL.

CPAL requires;
-The jsonrfclib library available here:
  https://pypi.python.org/pypi/jsonrpclib
-The configobj library available here:
  http://www.voidspace.org.uk/python/configobj.html

Requires the SUDS lightweight SOAP Python client (v0.4+) available here:
https://fedorahosted.org/suds/ if using Python v2.x.

Requires the SUDS-Jurko lightweight SOAP Python client available here:
https://pypi.python.org/pypi/suds-jurko if using Python v3.x.

Requires F5's BigSuds Python iControl library available here:
https://devcentral.f5.com/d/bigsuds-python-icontrol-library?download=true
(an account might be required).

I'd recommend you install the above using Python SetupTools available here:
https://pypi.python.org/pypi/setuptools.
'''
__author__ = 'Steven Iveson'

import bigsuds

class f5():
		
		def __init__(self,ip_address,obj):
			self.username = 'admin'
			self.password = 'admin'
			self.obj = obj
			self.address = ip_address
			self.native = self.jconnect() 

		def jconnect(self):

			try:
				lb = bigsuds.BIGIP(hostname=self.address,username=self.username,password=self.password)

			except  Exception, e:
			    print e
			    print 'Unable to connect to device.'	

			return lb
			
                def getUptime(self):
                        uptimenoformat = self.native.System.SystemInfo.get_uptime()
                        uptimeformat = "%s Seconds" % uptimenoformat
                        return uptimeformat

                def getVersion(self):
                        return self.native.System.SystemInfo.get_version()

                def getBaseMAC(self):
                        return self.native.System.SystemInfo.get_base_mac_address()

                def getPlatform(self):
                        return self.native.System.SystemInfo.get_marketing_name()

                def getTime(self):
                        timenoformat = self.native.System.SystemInfo.get_time()
                        timeformat = "%s:%s:%s" % (timenoformat['hour'], timenoformat['minute'], timenoformat['second'])
                        return timeformat

                def getTimeZone(self):
                        timezonenoformat = self.native.System.SystemInfo.get_time_zone()
                        timezoneformat = timezonenoformat['time_zone']
                        return timezoneformat

                def getBootLocation(self):
                        return self.native.System.SoftwareManagement.get_boot_location()
                        
                def getserialNumber(self):
                        return self.native.System.SystemInfo.get_system_id()

		def getHostname(self):
			return self.native._hostname

		def getFacts(self):
                        uptime = self.getUptime()
                        platform = self.getPlatform()
                        version = self.getVersion()
                        basemac = self.getBaseMAC()
                        serial = self.getserialNumber()
			hostname = self.getHostname()
			time = self.getTime()
			bootloc = self.getBootLocation()
			timezone = self.getTimeZone()

			facts = {'Hostname': hostname,'Platform': platform,'Version': version,'Boot_Location': bootloc,'Base_MAC': basemac,'Uptime': uptime,'S/N': serial,'Time': time,'Timezone': timezone}

			return facts

