#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import socket

class SocketConnection:
#implements Hellow_Core_ConnectionHandle{

	def __init__(self):
		self._socket = None
		self._buffer = ""


	def getSocket(self):
		#if (self._socket < 0):
		#	self.disconnect()
		return self._socket;

	def connect(self, host, port):
		port = long(port)
		print host, port
		if self.getSocket() != None:
			self._socket.close()
			self._socket = None;
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = self._socket.connect((host,port))
		#if ($this->getSocket()) {
		#	socket_close($this->_socket);
		#	$this->_socket == null;
		#}
		#$this->_socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		#$result = socket_connect($this->_socket, $host, $port);

	def disconnect(self):
		pass


#	public function disconnect() {
#		if ($this->_socket) {
#			socket_close($this->_socket);
#			$this->_socket = null;
#		} else {
#			$this->_socket = null;
#		}
#	}

	def send(self, cmd):
		if self.getSocket() != None:
			print cmd
			self.getSocket().send(cmd)

#	public function send($cmd) {
#		if ($this->getSocket()) {
#			socket_write($this->getSocket(), $cmd, strlen($cmd));
#			flush();
#		}
#	}

#//TODO: fix payloads->http://www.hypothetic.org/docs/msn/resources/faq.php#howtoparse

	def nextCommand(self):
		if self.getSocket != None:
			data = self._socket.recv(2048)
			print data
			cmd = data[:3]
			return data
		pass

#	public function nextCommand() {
#		if ($this->getSocket()) {
#			$command = socket_read($this->_socket, 2048, PHP_NORMAL_READ);
#			$cmd = substr($command, 0, 3);			
#			if ($cmd == 'MSG') {
#				$command_aux = explode(' ', $command);
#				$bytes = intval($command_aux[sizeof($command_aux) - 1]);
#				$payload = socket_read($this->getSocket(), $bytes);
#				$command .= $this->EL. $payload;
#			}
#		}
#		return $command;
#	}

	def hasMoreCommands(self):
		return True

#	public function hasMoreCommands(){
#		return true;
#	}
#}
