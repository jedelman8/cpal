class counter():
		
		
		def __init__(self):

			self.c = {}
			self.d = {}

		def calc(self,obj,address,hostname):

			self.d = {'hostname':hostname,'ip_address':address}
			self.c[obj] = self.d
			return self.c

