#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import SocketConnection


class Msnp:
    
    def __init__(self):
        self.EL = "\r\n"
        self._trid = 1
        self._connection = None
        self._commandListener = None
        self._connectionHandle = None
        self._connectionHandle = SocketConnection.SocketConnection()
    
    def setConnectionHandle(self, connectionHandle):
        self._connectionHandle = connectionHandle
    
    def addCommandListener(self, commandListener):
        self._commandListener = commandListener

    def onCommandReceived(self, command):
        if self._commandListener != None: self._commandListener.onCommandReceived(command)
    
    def onCommandSended(self, command):
        if self._commandListener != None: self._commandListener.onCommandSended(command)

    #abstract function getHost();
    #abstract function getPort();
    #abstract function execute($command);

    def send(self, command):
        self._connectionHandle.send(command)
        self.onCommandSended(command)
        self._trid += 1

    def _connect(self, host, port):
        self._connectionHandle.connect(host, port)
        
    def disconnect(self):
        self._connectionHandle.disconnect()

    def listen(self):
        while self._connectionHandle.hasMoreCommands():
            command = self._connectionHandle.nextCommand()
            if command != None and command != "":
                self.execute(command)
                self.onCommandReceived(command)
