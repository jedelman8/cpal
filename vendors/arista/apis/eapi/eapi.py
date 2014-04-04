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
from cpal.scripts.utils import convertSize
# from datetime import datetime

class arista():

    def __init__(self, address, obj):
        self.username = 'arista'
        self.password = 'arista'
        self.address = address
        self.obj = obj
        self.native = self.jconnect()
        self.facts = {}
        self.version_info = {}

        # self.version = self.getVersionInfo() must be place here
        # after call to jconnect() and before getFacts()
        #self.version_info = self.getVersionInfo()

        #self.facts = self.refreshFacts()

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
        #output = self.getCmd('show version')
        if not self.version_info:
            self.getVersionInfo()

        return self.version_info[0]["modelName"]

    def getserialNumber(self):
        #output = self.getCmd('show version')

        if not self.version_info:
            self.getVersionInfo()
        elif self.version_info[0]["serialNumber"] == '':
            return '12345'
        else:
            return self.version_info[0]["serialNumber"]

    def getUptime(self):
        output = self.native.runCmds( 1, ["show uptime"],"text")
        c = output[0]['output']
        up_time = c[13:].split(',')[0]
        return up_time

    def getCPU(self):
        output = self.native.runCmds(1, ['show processes top once'], 'text')
        # cpu = index 0 of returned list  split by new-lines
        # grabs the 3rd line which contains Cpu values at index [2]
        cpu_line = output[0]['output'].split('\n')[2]

        # cpu is then narrowed down to the actual usage, up to the first instance of a comma ','
        cpu = cpu_line[0:cpu_line.find(',')]
        return cpu

    def getHostname(self):
        ''' Returns the device's none FQDN hostname '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self.getCmd("show hostname")
            hostname = output[0]['hostname']
        else:
            # begins a breakdown of finding the hostname inside a string
            # could probably be more efficient, but works for now
            output = self.native.runCmds(1, ['show lldp local-info'], 'text')

            # gets the 4th line of output which contains the hostname in FQDN format
            host_line = output[0]['output'].split('\n')[3]

            # splits the line into a list at the delimeter and assigns the 2nd indext to fqdn
            # 2nd index contains the hostname
            host_fqdn = host_line.split(':')[1]

            # assignes the first index of fqdn after splitting at the delimeter (.)
            # this splits the fqdn into three parts, the [hostname, domain, suffix]
            hostname = host_fqdn.split('.')[0]

            # indexing removes the " from the begining of the hostname
            return hostname[2:]


        return hostname

    def getFQDN(self):
        ''' 
            Returns the device's FQDN hostname.domain.suffix
            has not been added to main.py yet, waiting to make sure 
            their's support accross platforms
        '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self.getCmd("show hostname")
            hostname = output[0]['fqdn']

        else:
            # begins a breakdown of finding the hostname inside a string
            # could probably be more efficient, but works for now
            output = self.native.runCmds(1, ['show lldp local-info'], 'text')

            # gets the 4th line of output which contains the hostname in FQDN format
            host_line = output[0]['output'].split('\n')[3]

            # splits the line into a list at the delimeter and assigns the 2nd indext to fqdn
            # 2nd index contains the hostname
            hostname = host_line.split(':')[1]

            # indexing removes the quotes (") from the begining and end of the hostname
            return hostname[2:-1]


        return hostname

    def getfreeMemory(self):
        #output = self.getCmd('show version')

        # checks if self.version_info is not empy
        if not self.version_info:
            self.getVersionInfo()

        return self.version_info[0]['memFree']

    def gettotalMemory(self):
        #output = self.getCmd('show version')

        # checks if self.version_info is not empy
        if not self.version_info:
            self.getVersionInfo()

        return self.version_info[0]['memTotal']

    # getVersionInfo created to streamline the calling of "show version"
    # there was allot of code that repeated it, this way, only one call is needed
    # speeds up the process and makes it more efficient.
    def getVersionInfo(self):
        ''' returns a 'show version' output as a dictionary '''
        
        self.version_info = self.getCmd('show version')
        return self.version_info

    def _versionList(self):
        ''' 
            Gets version and converts to a list of Ivalues
            this allows comparisons between software versions
            by calling int(on an index)
        '''
        version_list = self.version_info[0]['version'].split('.')
        return version_list

    def getVersion(self):
        ''' Returns the device running code version as a string '''

        # checks if self.version_info is not empy
        if not self.version_info:
            self.getVersionInfo()
            
        return self.version_info[0]['version']

    def getFacts(self):

        # moved getVersionInfo() so this information gets refreshed as well
        # and to remove the redundancy of __init__
        self.getVersionInfo()

        sh_ver = self.getVersion()
        #sh_lldp_localinfo = self.native.runCmds( 1, ["show lldp local-info"],"text")
        cpu_utilization = self.getCPU()
        free_memory = self.getfreeMemory()
        total_memory = self.gettotalMemory()
        uptime = self.getUptime()
        platform = self.getPlatform()
        serial_number = self.getserialNumber()
        connect_ip = self.address
        hostname = self.getHostname()

        var_name = self.obj

        self.facts = {'hostname': hostname, 'connect_ip': connect_ip, 'platform':platform, 'version':sh_ver,\
            'serial_number':serial_number, 'system_uptime':uptime, 'cpu_utilization':cpu_utilization, \
            'free_system_memory': free_memory, 'total_sytem_memory': total_memory, 'vendor':'arista', 'var_name':var_name}

        config = ConfigObj('/home/cisco/apps/cpal/core/device_tags.ini').dict()
        for key in config.keys():
            if key == self.address:
                self.facts.update(config[key])

        return self.facts
