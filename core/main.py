#!/usr/bin/env python
'''
This is the main module of the common programmable abstraction layer. It
returns a data structure of type 'device.' Ultimately, it is passing back
the native device type of said vendor API. For example, it returns a NE for
Cisco onePK and returns the main device for Arista eAPI (switch = Server(connection_parameters)).
It's basically returning 'switch.' __init__ calls the right vendor API and
gathers device facts. It is also returns a global list of connected_devices.
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
#from cpal.vendors.cisco.apis.onepk.onepk import cisco
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
            self.facts = self.getFacts()
        elif self.manufacturer.lower() == 'f5':
            self._thisdevice = f5(self.address,self.obj)
            self.native = self._thisdevice.native
            self.facts = self._thisdevice.getFacts()

        self.connected_devices = tracker.calc(self.obj,self.address,self.facts['hostname'])

    # sets the username and password if specified, otherwise uses default
    # method must exist in individual platform apis.
    def setLogin(self, username, password):
        self._thisdevice.setLogin(username, password)

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
        # Testing to prevent AttributeError to be thrown when trying to call
        # a function that is not in the specific device/API being used.  
        # This works...will add to other functions in the coming week

        '''if getattr(self._thisdevice,'getBaseMAC',None):
            value = self._thisdevice.getBaseMAC()
        else:
            value = '*** function does not exist for specified device (API) ***'

        return value '''

        return self._thisdevice.getBaseMAC() if getattr(self._thisdevice,'getBaseMAC',None)\
            else '*** function does not exist for specified device (API) ***'

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
        
    def getInterfaceNumber(self):
        return self._thisdevice.getInterfaceNumber() if getattr(self._thisdevice,'getInterfaceNumber',None)\
            else '*** getInterfaceNumber function does not exist for specified device (API) ***'
            
    def getVLANNumber(self):
        return self._thisdevice.getVLANNumber() if getattr(self._thisdevice,'getVLANNumber',None)\
            else '*** getVLANNumber function does not exist for specified device (API) ***'
            
    def getIPNumber(self):
        return self._thisdevice.getIPNumber() if getattr(self._thisdevice,'getIPNumber',None)\
            else '*** getIPNumber function does not exist for specified device (API) ***'
            
    def getTunnelNumber(self):
        return self._thisdevice.getTunnelNumber() if getattr(self._thisdevice,'getTunnelNumber',None)\
            else '*** getTunnelNumber function does not exist for specified device (API) ***'

    def d(self):
        self._thisdevice.disconnect()
        print 'Disconnected'

def createDevice(p_args):

    # sets dev_name if -n is used, otherwise generic 'dev' is used
    dev_name = p_args['name'] if p_args['name'] else 'dev'
    dev = device(dev_name, p_args['manufacturer'], p_args['ip_address'])

    if p_args['username'] and p_args['password']:
        dev.setLogin(p_args['username'], p_args['password'])
    
    # sets the function based on the command-line argument passed -f or -c
    function = p_args['function'] if p_args['function'] else p_args['cli']
    value = getattr(dev, function)()

    # prettifies the printing a bit, in case the returned value is 
    # more complex than a string
    if type(value) is dict:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(value)
    else:
        print value
    
    if args['manufacturer'] == 'cisco':
        dev.native.disconnect()

def display():
    print '********************************************************'
    print '***IP Address (-i), manufacturer (-m), AND one of*******'
    print '***the following functions (-f) are required************'
    print "***Use 'python main.py -h' for more info on proper usage"
    print '********************************************************'
    funcs = dir(device)
    for each in funcs:
        if not (each.startswith('__') or each == 'd' or each == 'deviceCalls'):
            print '*** '+each

    
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
    parser.add_argument('-d', '--display', help='Displays tasks that can be executed')

    args = vars(parser.parse_args())
    
    #print args
    if args['display'] or args['ip_address'] == None or args['manufacturer'] == None:
        display()
    elif args['function'] == None and args['cli'] == None:
        display()
    else:
        createDevice(args)
 