#!/usr/bin/env python

#   ------------------------------------------------------------------
#   Arista eAPI CPAL Integration
#
#   Written by: 
#       Jason Edelman
#   Updated by: 
#       Yandy Ramirez, @IP_Yandy
#   ------------------------------------------------------------------


from jsonrpclib import Server
from configobj import ConfigObj
# from datetime import datetime

class arista():

    def __init__(self, address,obj):
        self.username = 'arista'
        self.password = 'arista'
        self.address = address
        self.obj = obj
        self.native = self.jconnect()
        self.facts = self.getFacts()

    def jconnect(self):

        connect_string = "https://" + self.username + ":" + self.password + "@" + self.address + "/command-api"

        switch = 'DNE'
        try:
            switch = Server(connect_string)
        except Exception, e:
            print e
            print 'Unable to connect to device.'

        return switch

    def getCmd(self,cmd):
        return self.native.runCmds( 1, [cmd] )

    def getPlatform(self):
        output = self.getCmd('show version')
        return output[0]["modelName"]

    def getserialNumber(self):
        output = self.getCmd('show version')
        if output[0]["serialNumber"] == '':
            return '12345'
        else:
            return output[0]["serialNumber"]

    def getUptime(self):
        output = self.native.runCmds( 1, ["show uptime"],"text")
        c = output[0]['output']
        up_time = c[13:].split(',')[0]
        return up_time

    def getHostname(self):
        output = self.getCmd("show hostname")
        hostname = output[0]['hostname']
        return hostname

    def getfreeMemory(self):
        output = self.getCmd('show version')
        return output[0]['memFree']

    def gettotalMemory(self):
        output = self.getCmd('show version')
        return output[0]['memTotal']

    def getFacts(self):
        #sh_ver = self.native.runCmds( 1, ["show version"] )
        sh_uptime = self.native.runCmds( 1, ["show uptime"],"text" )
        #sh_lldp_localinfo = self.native.runCmds( 1, ["show lldp local-info"],"text")
        #cpu_utilization = self.getCPU(ne)
        free_memory = self.getfreeMemory()
        total_memory = self.gettotalMemory()
        uptime = self.getUptime()
        platform = self.getPlatform()
        serial_number = self.getserialNumber()
        connect_ip = self.address
        hostname = self.getHostname()

        var_name = self.obj

        facts = {'hostname': hostname, 'connect_ip': connect_ip,'platform':platform, 'serial_number':serial_number, 'system_uptime':uptime,'free_system_memory': free_memory,
            'total_sytem_memory': total_memory,'vendor':'arista','var_name':var_name}

        config = ConfigObj('/home/cisco/apps/cpal/core/device_tags.ini').dict()
        for key in config.keys():
            if key == self.address:
                facts.update(config[key])

        return facts

