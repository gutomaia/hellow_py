#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import unittest
import MockConnection
import MockClient
import MockAuthentication
import Msnp8


class ProtocolTest(unittest.TestCase):
    def setUp(self):
        self.mockClient = MockClient.MockClient()
        self.mockAuth = MockAuthentication.MockAuthentication()
        self.mockConnection = MockConnection.MockConnection()
        self.msn = Msnp8.Msnp8()
        self.msn.setAuthenticationHandle(self.mockAuth)
        self.msn.setConnectionHandle(self.mockConnection)
        #self.msn.addConnectionListener(self.mockClient)
        self.msn.addContactListener(self.mockClient)
        self.msn.login("dvader@empire.com", "ih8jedis")

    def receive(self, msg):
        self.msn.execute(msg)
    
    def send(self, msg):
        self.assertEquals(msg, self.mockConnection.sended)

    def testChallenger(self):
	    chl = '29409134351025259292'
        digest = self.msn.challenger(chl)
        self.assertEquals('d0c1178c689350104350d99f8c36ed9c', digest)

    def testSession(self):
        #Sends the MSN Client version
        self.send("VER 1 MSNP8 CVR0\r\n")
        
		#Acknowledge
		self.receive("VER 1 MSNP8 CVR0\r\n")
		self.send("CVR 2 0x0409 win 4.10 i386 MSNMSGR 6.0.0602 MSMSGS dvader@empire.com\r\n")
		
        #Client sends information
        self.receive("CVR 2 6.0.0602 1.0.000 http://download.microsoft.com/download/8/a/4/\r\n")
        self.send("USR 3 TWN I dvader@empire.com\r\n")

        #Redirect
        self.receive("XFR 3 NS 207.46.106.118:1863 0 207.46.104.20:1863\r\n")
        self.send("VER 4 MSNP8 CVR0\r\n")
        self.assertEquals("207.46.106.118",self.mockConnection.host, "Invalid host")
        self.assertEquals("1863", self.mockConnection.port, "Invalid port")
        
        self.receive("VER 4 MSNP8 CVR0\r\n")
        self.send("CVR 5 0x0409 win 4.10 i386 MSNMSGR 6.0.0602 MSMSGS dvader@empire.com\r\n")
        self.receive("CVR 5 6.0.0602 6.0.0602 1.0.0000 http://download.microsoft.com/download/8/a/4/8a42bcae-f533-4468-b871-d2bc8dd32e9e/SETUP9x.EXE http://messenger.msn.com\r\n")
        self.send("USR 6 TWN I dvader@empire.com\r\n")

        self.receive("USR 6 TWN S lc=1033,id=507,tw=40,fs=1,ru=http%3A%2F%2Fmessenger%2Emsn%2Ecom,ct=1062764229,kpp=1,kv=5,ver=2.1.0173.1,tpf=43f8a4c8ed940c04e3740be46c4d1619\r\n")
        self.send("USR 7 TWN S t=53*1hAu8ADuD3TEwdXoOMi08sD*2!cMrntTwVMTjoB3p6stWTqzbkKZPVQzA5NOt19SLI60PY!b8K4YhC!Ooo5ug$$&p=5eKBBC!yBH6ex5mftp!a9DrSb0B3hU8aqAWpaPn07iCGBw5akemiWSd7t2ot!okPvIR!Wqk!MKvi1IMpxfhkao9wpxlMWYAZ!DqRfACmyQGG112Bp9xrk04!BVBUa9*H9mJLoWw39m63YQRE1yHnYNv08nyz43D3OnMcaCoeSaEHVM7LpR*LWDme29qq2X3j8N\r\n")
        self.assertFalse(self.mockClient.logged, "User not logged, ConnectionListener::onLogged shoudn't be called")

        #Logged
        self.receive("USR 7 OK dvader@empire.com Dart%20Vader 1 0\r\n")
        #$this->assertTrue($this->_mockClient->logged, "User logged, ConnectionListener::onLogged should be called");
        self.send("SYN 1 0\r\n")

        self.receive("SYN 8 27 5 4\r\n")
        self.receive("GTC A\r\n")
        self.receive("BLP AL\r\n")
        self.receive("PRP PHH O1%20234\r\n")
        self.receive("PRP PHM 56%20789\r\n")
        self.assertEquals(self.mockClient.group, None)
        self.receive("LSG 0 Sifth\r\n")
        self.assertEquals(self.mockClient.group['group_id'], '0')
        self.assertEquals(self.mockClient.group['name'], 'Sifth')
        self.receive("LSG 1 Jedis\r\n")
        self.assertEquals(self.mockClient.group['group_id'], '1')
        self.assertEquals(self.mockClient.group['name'], 'Jedis')

        #Add Emperor as a contact
        self.assertEquals(self.mockClient.contact, None)
        self.receive("LST emperor@empire.com Emperor 13 0\r\n")
        self.assertEquals(self.mockClient.contact['user'], 'emperor@empire.com')
        self.assertEquals(self.mockClient.contact['nick'], 'Emperor')
        self.assertEquals(self.mockClient.contact['lists'], '13')
        #self.assertEquals(self.mockClient.contact['groups'], '0');

        self.receive("BPR MOB Y\r\n")

		#Add Luke as a contact
        self.receive("LST luke@rebels.org Luke 3 1\r\n")
        self.assertEquals(self.mockClient.contact['user'], 'luke@rebels.org')
        self.assertEquals(self.mockClient.contact['nick'], 'Luke')
        self.assertEquals(self.mockClient.contact['lists'], '3') #Luke dosen't have Vader in their list! Bastard!!
        #self.assertEquals(self.mockClient.contact['groups'], '1')

		#self.send("CHG 9 NLN 0\r\n")
        self.receive("CHG 9 NLN 0\r\n")

        #//Initial Presence
        self.receive("ILN 9 NLN emperor@empire.com Emperor 24\r\n")
        self.receive("ILN 9 IDL luke@rebels.org Luke 268435492\r\n")

        #//Challenger
        self.receive("CHL 0 29409134351025259292\r\n");
		self.send("QRY 10 msmsgs@msnmsgr.com 32\r\nd0c1178c689350104350d99f8c36ed9c");
        
        #//Presence
        #$this->receive("NLN NLN luke@rebels.org Luke%20JediMaster 268435492\r\n");//Available
        #$this->receive("NLN BSY luke@rebels.org Luke%20JediMaster 268435492\r\n");//Busy
        #$this->receive("NLN IDL luke@rebels.org Luke%20JediMaster 268435492\r\n");//Idle
        #$this->receive("NLN BRB luke@rebels.org Luke%20JediMaster 268435492\r\n");//Be Right Back
        #$this->receive("NLN AWY luke@rebels.org Luke%20JediMaster 268435492\r\n");//Away
        #$this->receive("NLN PHN luke@rebels.org Luke%20JediMaster 268435492\r\n");//On the Phone
        #$this->receive("NLN LUN luke@rebels.org Luke%20JediMaster 268435492\r\n");//Out to lunch
        #$this->receive("FLN luke@rebels.org\r\n");
        #$this->receive("FLN emperor@empire.com\r\n");

        #// Call
        #$this->receive("RNG 876505971 65.54.228.15:1863 CKI 4216622.2513084 emperor@empire.com Emperor");
        #//$this->assertEquals("876505971", $this->mockCall->call);
        #//$this->assertEquals("65.54.228.15", $this->mockCall->server);
        #//$this->assertEquals(1863, $this->mockCall->port);
        #//$this->assertEquals("4216622.2513084", $this->mockCall->cki);
        #//$this->assertEquals("emperor@empire.com", $this->mockCall->username);
        #//$this->assertEquals("Emperor", $this->mockCall->nick);

if __name__=="__main__":
    unittest.main()
