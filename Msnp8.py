#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributable under the terms of an GPLv3 licence.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import Msnp
import Notification


class Msnp8(Notification.Notification):

    def __init__(self):
        Notification.Notification.__init__(self)
        #super(Msnp8,self).connect()
        self.MSN_HOST = 'messenger.hotmail.com'
        self.MSN_PORT = 1863
        self.PROTOCOL_VERSION = 'MSNP8'
        self.LOCALE_ID = '0x0409'

        self.OS_TYPE = 'win'
        self.OS_VERSION = '4.10'
        self.CPU_ARCHITECTURE = 'i386'
        self.CLIENT_NAME = 'MSNMSGR'
        self.CLIENT_VERSION = '6.0.0602'

        #Challenger

        self.CLIENT_ID = 'MSMSGS'
        self.CLIENT_IDCODE = 'msmsgs@msnmsgr.com'
        self.CLIENT_CODE = 'Q1P7W2E4J9R8U3S5'; #needed for the chalenger

    def execute(self, command):
        cmd = command[:3]
        if cmd == 'VER':
            self.send(self.cvr())
        elif cmd == "CVR":
            self.send(self.usr())
        elif cmd == "XFR":
            host_port = command.split(' ')[3].split(':')
            host = host_port[0]
            port = host_port[1]
            self.connect(host, port)
        elif cmd == "USR":
            params = command.split(' ')
            if params[2] == "TWN":
                self.authenticate(params[4])
                self.send(self.usr())
            elif params[2] == "OK":
                #self.onLogged()
                self.send(self.syn())
        elif cmd == "SYN":
            self.send(self.chg)
#       elif cmd == "GTC":
#       elif cmd == "BLP":
#       elif cmd == "PRP":
        elif cmd == "LSG":
            params = command.strip().split(' ')
            if len(params) == 4:
                self.onAddGroup(params[1], params[2], params[3])
            else:
                self.onAddGroup(params[1], params[2])
        elif cmd == "LST":
            params = command.strip().split(' ')
            if len(params) == 5:
                self.onAddContact(params[1], params[2], params[3], params[3])
            else:
                self.onAddContact(params[1], params[2], params[3])
#       elif cmd == "PHH":
#       elif cmd == "PHW":
#       elif cmd == "MOB":
#       elif cmd == "MBE":
#       elif cmd == "BPR":
#       elif cmd == "ILN":
#       elif cmd == "FLN":
#       elif cmd == "NLN":
#       elif cmd == "MSG":
#       elif cmd == "RNG":
#$this->onRing($params[1], $params[2], $params[3], $params[4], $params[5], $params[6]);
        elif cmd == "CHG":
            self.onConnected()
        elif cmd == "CHL":
            params = command.strip().split(' ')
            self.send(self.qry(params[2]))
        #   elif cmd == "QRY":
        elif cmd == "207":  
            self.disconnect()
