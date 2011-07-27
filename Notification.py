#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import Msnp
import Tweener
import hashlib


class Notification(Msnp.Msnp):

    def __init__(self):
        Msnp.Msnp.__init__(self)
        self._authenticationHandle = Tweener.Tweener()
        self._username = None
        self._password = None
        self._passport = None
        self._connectionListener = None
        self._contactListener = None
        self._presenceListener = None
        self._callListener = None

    def setAuthenticationHandle(self, authenticationHandle):
        self._authenticationHandle = authenticationHandle
    
    def authenticate(self, lc):
        self._passport = self._authenticationHandle.authenticate(self._username, self._password, lc)

    def connect(self, host, port):
#        if (self._username == None || self._password == None):
    #    super(type(Notification), self).connect(host, port)
    #    super(Notification, self).connect(host,port)
        self._connect(host,port)
        self.send(self.ver())
        self.listen()
    
    def login(self, username, password):
        self._username = username
        self._password = password
        self.connect(self.MSN_HOST, self.MSN_PORT)

    def logout(self):
        self.send(self.out())
        self.disconnect()

#    public final function addConnectionListener($connectionListener){
#        $this->_connectionListener = $connectionListener;

#    public final function 
    def addContactListener(self, contactListener):
        self._contactListener = contactListener
#        $this->_contactListener = $contactListener;

#    public final function addPresenceListener($presenceListener){
#        $this->_presenceListener = $presenceListener;

#    public final function addCallListener($callListener){
#        $this->_callListener = $callListener;


    #Connection
    #protected final function onLogged(){if(!empty($this->_connectionListener)) $this->_connectionListener->onLogged();}
    #protected final 
    def onConnected(self):
        if self._connectionListener != None:
            self._connectionListener.onConnected()

    #Contact
    #protected final function 
    def onAddContact(self, user, nick, lists, groups = None):
        if self._contactListener != None:
            contact = {'user':user, 'nick':nick, 'lists':lists, 'groups':groups}
            self._contactListener.onAddContact(contact)

    #protected final function onRemoveContact($user){if(!empty($this->_contactListener)) $this->_contactListener->onRemoveContact($user);}
    #protected final 
    def onAddGroup(self, id, name, unk = None):
        if self._contactListener != None:
            group = {'group_id':id, 'name':name}
            self._contactListener.onAddGroup(group)
    #protected final function onRemoveGroup($group){}

    #Presence
    #protected final function onContactOnline($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactOnline($contact);}
    #protected final function onContactOffline($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactOffline($contact);}
    #protected final    function onContactAvaiable($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactAvaiable($contact);}
    #protected final function onContactBusy($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactBusy($contact);}
    #protected final function onContactIdle($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactIdle($contact);}
    #protected final function onContactBeRightBack($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactBeRightBack($contact);}
    #protected final function onContactAway($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactAway($contact);}
    #protected final function onContactOnPhone($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactOnPhone($contact);}
    #protected final function onContactOutLunch($contact){if(!empty($this->_presenceListener)) $this->_presenceListener->onContactOutLunch($contact);}

    #Call
    #protected final function onRing($call, $server, $port, $cki, $username, $nick){
    #    if(!empty($this->_callListener)) $this->_callListener->onRing($call, $server, $port, $cki, $username, $nick);

    def ver (self):
        return 'VER {0} {1} CVR0{2}'.format(self._trid, self.PROTOCOL_VERSION, self.EL)
    #    return "VER "+self._trid+" "+self.PROTOCOL_VERSION+" CVR0"+self.EL

    def cvr (self):
        return "CVR {0} {1} {2} {3} {4} {5} {6} {7} {8}{9}".format(self._trid,self.LOCALE_ID,self.OS_TYPE,self.OS_VERSION,self.CPU_ARCHITECTURE, self.CLIENT_NAME, self.CLIENT_VERSION, self.CLIENT_ID, self._username, self.EL)
        #return "CVR " . $this->_trid . " " . $this->getLocale() . " " .    $this->getOSType() . " " . $this->getOSVersion() . " " .
        #$this->getArch() . " " . $this->getClientName() . " " .    $this->getClientVersion() . " " . $this->getClientId() . " " .

    def usr (self):
        if self._passport == None:
            return "USR {0} TWN I {1}{2}".format(self._trid, self._username, self.EL)
        else:
            return "USR {0} TWN S {1}{2}".format(self._trid, self._passport, self.EL)

    def syn (self):
        return "SYN 1 0" + self.EL
    
    def chg (self):
        return "CHG " + self._trid + " NLN 0" + self.EL

    def qry (self, chl = None):
        return "QRY {0} {1} 32{2}". format(self._trid, self.CLIENT_IDCODE, self.EL+self.challenger(chl))

    def challenger(self, chl):
        md5 = hashlib.md5()
        md5.update(chl)
        md5.update(self.CLIENT_CODE)
        return md5.hexdigest()

    def out():
        return "OUT" + self.EL

