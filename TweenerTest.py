#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import unittest
import Tweener

class TweenerTest(unittest.TestCase):

    def setUp(self):
        self._twn = Tweener.Tweener()
        self.EL = "\r\n"
    
    def tearDown(self):
        self._twn = None

    def testExtractHttpResponseHeader(self):
        self.assertTrue(True)
        header = 'HTTP/1.1 200 OK' + self.EL
        header += 'Date: Sun, 11 Jul 2010 18:46:58 GMT' + self.EL
        header += 'Server: Microsoft-IIS/6.0' + self.EL
        header += 'PPServer: PPV: 30 H: BAYIDSPRTS1B04 V: 0' + self.EL
        header += 'PassportURLs: DARealm=Passport.Net,DALogin=login.live.com/login2.srf,DAReg=https://accountservices.passport.net/UIXPWiz.srf,Properties=https://accountservices.msn.com/editprof.srf,Privacy=https://accountservices.passport.net/PPPrivacyStatement.srf,GeneralRedir=http://nexusrdr.passport.com/redir.asp,Help=https://accountservices.passport.net,ConfigVersion=14' + self.EL
        header += 'Content-Length: 0' + self.EL
        header += 'Content-Type: text/html' + self.EL
        header += 'Cache-control: private' + self.EL
        header += self.EL
        props = self._twn.extractHttpResponseHeader(header)
        self.assertEquals('Sun, 11 Jul 2010 18:46:58 GMT', props['Date'], 'Date not equals')
        self.assertEquals('Microsoft-IIS/6.0', props['Server'], 'Server not equals')
        self.assertEquals('PPV: 30 H: BAYIDSPRTS1B04 V: 0', props['PPServer'], 'PPServer not equals')
        self.assertEquals('DARealm=Passport.Net,DALogin=login.live.com/login2.srf,DAReg=https://accountservices.passport.net/UIXPWiz.srf,Properties=https://accountservices.msn.com/editprof.srf,Privacy=https://accountservices.passport.net/PPPrivacyStatement.srf,GeneralRedir=http://nexusrdr.passport.com/redir.asp,Help=https://accountservices.passport.net,ConfigVersion=14', props['PassportURLs'], 'PassportURLs not equals')
        self.assertEquals('Sun, 11 Jul 2010 18:46:58 GMT', props['Date'], 'Date not equals')
        self.assertEquals('0', props['Content-Length'], 'Content-Length not equals')
        self.assertEquals('text/html', props['Content-Type'], 'Content-Type not equals')
        self.assertEquals('private', props['Cache-control'], 'Cache-control not equals')

    def testExtractPassportVars(self):
        passportURLs = 'ARealm=Passport.Net,DALogin=login.live.com/login2.srf,DAReg=https://accountservices.passport.net/UIXPWiz.srf,Properties=https://accountservices.msn.com/editprof.srf,Privacy=https://accountservices.passport.net/PPPrivacyStatement.srf,GeneralRedir=http://nexusrdr.passport.com/redir.asp,Help=https://accountservices.passport.net,ConfigVersion=14'
        props = self._twn.extractVarParams(passportURLs)
        self.assertEquals(props['ARealm'], 'Passport.Net','ARealm not equals')
        self.assertEquals(props['DALogin'], 'login.live.com/login2.srf', 'DALogin not equals')
        self.assertEquals(props['DAReg'],'https://accountservices.passport.net/UIXPWiz.srf', 'DAReg not equals')
        self.assertEquals(props['Properties'], 'https://accountservices.msn.com/editprof.srf', 'Properties not equals')
        self.assertEquals(props["Privacy"],'https://accountservices.passport.net/PPPrivacyStatement.srf', 'Privacy not equals')
        self.assertEquals(props['GeneralRedir'],'http://nexusrdr.passport.com/redir.asp', 'GeneralRedir not equals')
        self.assertEquals(props['Help'], 'https://accountservices.passport.net', 'Help not equals')
        self.assertEquals(props['ConfigVersion'], '14','ConfigVersion not equals')

    def testBuildParamVars(self):
        username = 'dvader%40empire.com'
        password = 'ih8jedis'
        lc = 'ct=1278901179,rver=5.5.4182.0,wp=FS_40SEC_0_COMPACT,lc=1033,id=507,ru=http:%2F%2Fmessenger.msn.com,tw=0,kpp=1,kv=4,ver=2.1.6000.1,rn=1lgjBfIL,tpf=b0735e3a873dfb5e75054465196398e0';
        expected = 'Passport1.4 OrgVerb=GET,OrgURL=http%3A%2F%2Fmessenger%2Emsn%2Ecom,sign-in={0},pwd={1},{2}'.format(username, password, lc)
        authParams = {
                'Passport1.4 OrgVerb':'GET',
                'OrgURL':'http%3A%2F%2Fmessenger%2Emsn%2Ecom',
                'sign-in':username,
                'pwd':password,
                'lc':lc
        }
        actual = self._twn.buildParamVars(authParams)
#        self.assertEquals(expected, actual)
    
    def testBuildHttpRequestHeader(self):
        expected = 'GET /login2.srf HTTP/1.1' + self.EL
        expected += 'Authorization: Passport1.4 OrgVerb=GET,OrgURL=http%3A%2F%2Fmessenger%2Emsn%2Ecom,sign-in=dvader%40empire.com,pwd=ih8jedis,ct=1278901179,rver=5.5.4182.0,wp=FS_40SEC_0_COMPACT,lc=1033,id=507,ru=http:%2F%2Fmessenger.msn.com,tw=0,kpp=1,kv=4,ver=2.1.6000.1,rn=1lgjBfIL,tpf=b0735e3a873dfb5e75054465196398e0' + self.EL
        expected +='Host: login.live.com' + self.EL
        expected += self.EL
        requestParams = {
                'Authorization':'Passport1.4 OrgVerb=GET,OrgURL=http%3A%2F%2Fmessenger%2Emsn%2Ecom,sign-in=dvader%40empire.com,pwd=ih8jedis,ct=1278901179,rver=5.5.4182.0,wp=FS_40SEC_0_COMPACT,lc=1033,id=507,ru=http:%2F%2Fmessenger.msn.com,tw=0,kpp=1,kv=4,ver=2.1.6000.1,rn=1lgjBfIL,tpf=b0735e3a873dfb5e75054465196398e0',
                'Host':'login.live.com'
        }
        requestHeader = self._twn.buildHttpRequestHeader('login.live.com/login2.srf', requestParams);
        #self.assertEquals(expected, requestHeader)

    def testEncode(self):
        username = 'dvader@empire.com'
        expected = 'dvader%40empire.com'
        actual = self._twn.encode(username)
        self.assertEquals(expected, actual)

if __name__=="__main__":
    unittest.main()
