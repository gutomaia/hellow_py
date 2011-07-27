#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

class MockClient:
#ConnectionListener, Hellow_Core_ContactListener {

    def __init__(self):
        self.logged = False
        self.connected = False
        self.group = None
        self.contact = None

    def onLogged(self):
        self.logged = True

    def onConnected(self):
        self.connected = True

    def onAddContact(self, contact):
        self.contact = contact

    def onRemoveContact(self, contact):
        pass

    def onAddGroup(self, group):
        self.group = group

    def onRemoveGroup(self, group):
        pass
