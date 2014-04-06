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

The configobj module is also required for writing to the device_tags.ini file
https://pypi.python.org/pypi/six
-this in turn requires the six module: https://pypi.python.org/pypi/six

I'd recommend you install the above using Python SetupTools available here:
https://pypi.python.org/pypi/setuptools.
'''
__author__ = 'Steven Iveson'

import bigsuds
from datetime import datetime, timedelta
from configobj import ConfigObj

class f5():
		
		def __init__(self,ip_address,obj):
			self.username = 'admin'
			self.password = 'T0pdoggie'
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

                        #Output is in seconds so adjust output accordingly
                        if uptimenoformat < 86400:
                            years = 0
                            days = 0
                            weeks = 0
                            sec = timedelta(seconds=uptimenoformat)
                            d = datetime(1,1,1) +sec
                            hours = d.hour
                            minutes = d.minute
                        else:
                            minutes, seconds = divmod(uptimenoformat, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            weeks, days = divmod(days, 7)
                            years, weeks = divmod(weeks, 365)
                            
                        if minutes <= 1:
                            minutesformat = str(minutes) + ' Minute'
                        else:
                            minutesformat = str(minutes) + ' Minutes'

                        if hours <= 1:
                           hoursformat = str(hours) + ' Hour'
                        else:
                            hoursformat = str(hours) + ' Hours'

                        if days <= 1:
                            daysformat = str(days) + ' Day'
                        else:
                            daysformat = str(days) + ' Days'

                        if weeks <= 1:
                            weeksformat = str(weeks) + ' Week'
                        else:
                            weeksformat = str(weeks) + ' Weeks'
 
                        if years <= 1:
                            yearsformat = str(years) + ' Year'
                        else:
                            yearsformat = str(years) + ' Years'

                        uptimeformat = '%s:%s:%s:%s:%s' % (yearsformat, weeksformat, daysformat, hoursformat, minutesformat)

                        return uptimeformat

                def getVersion(self):
                        return self.native.System.SystemInfo.get_version()

                def getBaseMAC(self):
                        return self.native.System.SystemInfo.get_base_mac_address()

                def getPlatform(self):
                        return self.native.System.SystemInfo.get_marketing_name()

                def getTime(self):
                        timenoformat = self.native.System.SystemInfo.get_time()
                        timezonenoformat = self.native.System.SystemInfo.get_time_zone()

                        timezoneoffset = timezonenoformat['gmt_offset']

                        hournoformat = timenoformat['hour']
                        minutenoformat = timenoformat['minute']
                        secondnoformat = timenoformat['day']
                        
                        #Output is UTC time only so lets add the offset as given by the timezone data
                        hourplustimezoneoffset = int(hournoformat) + int(timezoneoffset)

                        if hourplustimezoneoffset < 10:
                            #Add a leading zero if hour is a single digit
                            hourformat = '0' + str(hourplustimezoneoffset)
                        else:
                            hourformat = hourplustimezoneoffset

                        if minutenoformat < 10:
                            #Add a leading zero if minute is a single digit
                            minuteformat = "0" + str(minutenoformat)
                        else:
                            minuteformat = minutenoformat

                        if secondnoformat < 10:
                            #Add a leading zero if second is a single digit
                            secondformat = "0" + str(secondnoformat)
                        else:
                            secondformat = secondnoformat

                        #Colon format our adjusted data before it's returned
                        timeformat = "%s:%s:%s" % (hourformat, minuteformat, secondformat)
                        return timeformat

                def getTimeZone(self):
                        timezonenoformat = self.native.System.SystemInfo.get_time_zone()
                        #I also want to show the UTC offset of the timezone
                        timezoneoffset = timezonenoformat['gmt_offset']

                        #Specify + for the timezone UTC offset if zero or greater
                        if timezoneoffset >= 0:
                            negorpos = "+"
                        #Specify - for the timezone UTC offset if less than zero
                        else:
                            negorpos = "-"

                        #Format our output
                        return timezonenoformat['time_zone'] + " (UTC " + negorpos + str(timezoneoffset) + ")"

                def getBootLocation(self):
                        return self.native.System.SoftwareManagement.get_boot_location()

                def getserialNumber(self):
                        #This call returns quite a bit of information
                        systeminfo = self.native.System.SystemInfo.get_system_information()
                        #We just want the serial number
                        serialnumber = systeminfo['chassis_serial']
                        return serialnumber

		def getFQDN(self):
		        #This call always returns the FQDN so lets store in a variable for getHostname
                        fqdn = self.native.System.Inet.get_hostname()
			return fqdn

		def getHostname(self):
		        #Split FQDN using '.' as a delimiter, the hostname is the first field (zero indexed, hence [0])
                        fqdn = self.native.System.Inet.get_hostname()
		        return fqdn.split('.')[0]
		        
                def getInterfaces(self):
                        #This gets a list of all physical interfaces
                        interfaces = self.native.Networking.Interfaces.get_list()
                        return interfaces

                def getInterfaceNumber(self):
                        #This gets a list of all physical interfaces (Layer 1)
                        interfaces = self.native.Networking.Interfaces.get_list()
                        #We need to know how many there are for later operations
                        interfacenumber = len(interfaces)
                        return interfacenumber
                        
                        #Haven't quite worked out how to iterate through the list and display information on each
                        
                def getVLANNumber(self):
                        #This gets a list of all VLANs (Layer 2)
                        vlans = self.native.Networking.VLAN.get_list()
                        #We need to know how many there are for later operations
                        vlannumber = len(vlans)
                        return vlannumber
                        
                        #Haven't quite worked out how to iterate through the list and display information on each

                def getIPNumber(self):
                        #This gets a list of all Self IPs (Layer 3)
                        ips = self.native.Networking.SelfIPV2.get_list()
                        #We need to know how many there are for later operations
                        ipnumber = len(ips)
                        return ipnumber

                        #Haven't quite worked out how to iterate through the list and display information on each
                        
                def getTunnelNumber(self):
                        #This gets a list of all Tunnels (IPsec, Layer 4)
                        tunnels = self.native.Networking.Tunnel.get_list()
                        #We need to know how many there are for later operations
                        tunnelnumber = len(tunnels)
                        return tunnelnumber

                        #Haven't quite worked out how to iterate through the list and display information on each

		def setLogin(self, username, password):
			self.username = username
			self.password = password

		def getFacts(self):
                        uptime = self.getUptime()
                        platform = self.getPlatform()
                        version = self.getVersion()
                        basemac = self.getBaseMAC()
                        serial = self.getserialNumber()
			hostname = self.getHostname()
			interfaces = self.getInterfaces()
			interfacenumber = self.getInterfaceNumber()
			vlannumber = self.getVLANNumber()
			selfipnumber = self.getIPNumber()
			tunnelnumber = self.getTunnelNumber()
			fqdn = self.getFQDN()
			time = self.getTime()
			bootloc = self.getBootLocation()
			timezone = self.getTimeZone()

			var_name = self.obj

			facts = {'hostname': hostname,'FQDN': fqdn,'Platform': platform,'Version': version,'Boot_Location': bootloc,\
                          'Base_MAC': basemac,'Uptime': uptime,'S/N': serial,'Time': time,'Timezone': timezone,\
                          'Physical_Interfaces': interfacenumber,'Physical_Interfaces': interfaces,'VLANs': vlannumber,\
                          'Self_IPs': selfipnumber,'Tunnel_Number': tunnelnumber,'Vendor': 'F5 Networks','var_name':var_name}
   
                        config = ConfigObj('/c/cpal/core/device_tags.ini').dict()
                        for key in config.keys():
                            if key == self.address:
                                facts.update(config[key])

			return facts