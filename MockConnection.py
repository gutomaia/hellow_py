#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

class MockConnection:

	def __init__(self):
		self.sended = None
		self.reveiced = None
		self.host = None
		self.port = None
	
	def connect(self, host, port):
		self.host = host
		self.port = port
	
	def disconnect(self):
		pass

	def send(self, cmd):
		self.sended = cmd

	def receive(self,cmd):
		self.received = cmd
	
	def nextCommand(self):
		return None

	def hasMoreCommands(self):
		return False
