

import bigsuds

class f5():
		
		def __init__(self,ip_address,obj):
			self.username = 'admin'
			self.password = 'cisco'
			self.obj = obj
			self.address = ip_address
			self.native = self.jconnect() 

		def jconnect(self):

			try:
				lb = bigsuds.BIGIP('192.168.1.118',username=self.username,password=self.password)

			except  Exception, e:
			    print e
			    print 'Unable to connect to device.'	

			return lb
			
		def getPools(self):
			return self.native.LocalLB.Pool.get_list()

		def getHostname(self):
			return self.native._hostname

		def getFacts(self):
			hostname = self.getHostname()
			pools = self.getPools()

			facts = {'hostname': hostname,'pools': pools}

			return facts

