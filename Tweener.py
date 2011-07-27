#  HellowPy, alpha version
#  (c) 2011 Gustavo Maia Neto (gutomaia)
#
#  HellowPy and all other Hellow flavors will be always
#  freely distributed under the terms of an GPLv3 license.
#
#  Human Knowledge belongs to the World!
#--------------------------------------------------------------------------

import pycurl
import StringIO

class Tweener:
#implements Hellow_Core_Authentication{

    def __init__(self):
        self.EL = "\r\n"
        self.passportProps = None

    def extractHttpResponseHeader(self, httpResponse):
        props = {}
        cutter = httpResponse.find("\r\n\r\n")
        header = httpResponse[0:cutter]
        parameter_values = header.split(self.EL)
        for i in range(1, len(parameter_values)):
            cutter = parameter_values[i].find(':')
            key = parameter_values[i][0:cutter]
            value = parameter_values[i][cutter+2:]
            props[key] = value
        return props

    def extractVarParams(self, params):
        props = {}
        parameter_values = params.split(',')
        for parameter in parameter_values:
            cutter = parameter.find('=')
            key = parameter[:cutter]
            value = parameter[cutter+1:]
            props[key] = value
        return props

#    function extractVarParams($params) {
#        $props = array();
#        $parameters_values = explode(',',$params);
#        foreach($parameters_values as $parameter){
#            $cutter = strpos($parameter, "=");
#            $key = substr($parameter,0, $cutter);
#            $value = substr($parameter, $cutter+1,strlen($parameter) );
#            $props[$key] = $value;            
#        }
#        return $props;
#    }

    def connectToTheNexus(self):
        requestUrl = 'nexus.passport.com/rdr/pprdr.asp'
        httpRequest = self.buildHttpRequestHeader(requestUrl)
        httpResponse = self.request(requestUrl, 443, httpRequest)
        self.passportProps = {}
        #responseHeader = self.extractHttpResponseHeader(httpResponse)
        #passportURLs = responseHeader['PassportURLs']
        #self.passportProps = self.extractVarParams(passportURLs)
        self.passportProps['DALogin'] = 'login.live.com/login2.srf'

#    function connectToTheNexus() {
#        $requestUrl = 'nexus.passport.com/rdr/pprdr.asp';
#        $httpRequest = $this->buildHttpRequestHeader($requestUrl);
#        $httpResponse = $this->request($requestUrl, 443, $httpRequest);
#        $responseHeader = $this->extractHttpResponseHeader($httpResponse);
#        $passportURLS = $responseHeader['PassportURLs'];
#        $this->passportProps = $this->extractVarParams($passportURLS);
#    }

    def buildHttpRequestHeader(self, url, params = None):
        requestHeader = ''
        host = url[:url.find('/')]
        getRequest = url[url.find('/'):]
        if params == None:
            params = {}
        params['Host'] = host
        requestHeader += 'GET ' + getRequest + ' HTTP/1.1' + self.EL
        for key, value in params.iteritems():
            requestHeader += key + ': '+ value + self.EL
        return requestHeader

    def buildParamVars(self, params):
        paramVars = '';
        for key, value in params.iteritems():
            if key == 'lc':
                paramVars +=value
            else:
                paramVars +=key+'='+value
                paramVars +=','
        return paramVars

#    function buildParamVars($params){
#        $paramVars = '';
#        foreach($params as $paramKey=>$paramValue){
#            if ($paramKey=='lc'){
#                $paramVars.=$paramValue;
#            }else{
#                $paramVars.=$paramKey.'='.$paramValue;
#                $paramVars.=',';
#            }
#        }
#        return $paramVars;
#    }

    def encode(self, var):
        return var.replace('@', '%40')

#    function encode($var){
#        return str_replace("@", "%40", $var);
#    }

    def request(self, url, port, httpRequest):
        host = url[:url.find('/')]
        request = url[url.find('/'):]
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.VERBOSE, 1)
        response = StringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, response.write)
        curl.perform()
        return response.getvalue()

        #conn = httplib.HTTPSConnection(host)
        #conn.putrequest('GET', request)
        #conn.endheaders()
        #response = conn.getresponse()
        #httpResponse = response.msg
        #print httpResponse
        #return httpResponse

#        $host = ($port == 443)?'ssl://'.$host:$host;
#        $fp = fsockopen($host, $port, $errno, $errstr);
#        if (!$fp){
#            echo '>>>>ERRO'. $errno. ' '. $errstr.' '.$host;
#            exit();
#            //TODO: throw Exception;
#        }
#        $httpResponse = '';
#        fwrite($fp, $httpRequest);
#        while (!feof($fp)) {
#            $httpResponse .= fgets($fp, 128);
#        }
#        fclose($fp);

#    function request($url, $port, $httpRequest){
#        $host = substr($url, 0,strpos($url,'/'));
#        $host = ($port == 443)?'ssl://'.$host:$host;
#        $fp = fsockopen($host, $port, $errno, $errstr);
#        if (!$fp){
#            echo '>>>>ERRO'. $errno. ' '. $errstr.' '.$host;
#            exit();
#            //TODO: throw Exception;
#        }
#        $httpResponse = '';
#        fwrite($fp, $httpRequest);
#        while (!feof($fp)) {
#            $httpResponse .= fgets($fp, 128);
#        }
#        fclose($fp);
#        return $httpResponse;        
#    }
    pass

    def performTheLogin(self, username, password, lc):
        DALogin = self.passportProps['DALogin']
        authParams = {
                'Passport1.4 OrgVerb':'GET',
                'OrgURL':'http%3A%2F%2Fmessenger%2Emsn%2Ecom',
                'sign-in': self.encode(username),
                'pwd':self.encode(password),
                'lc':lc
        }
        authorization = self.buildParamVars(authParams)
        requestParams = {
                'Authorization':authorization
        }
        httpRequest = self.buildHttpRequestHeader(DALogin, requestParams)
        httpResponse = self.request(DALogin, 433, httpRequest)
        httpHeader = self.extractHttpResponseHeader(httpResponse)
        authenticationInfo = httpHeader['Authentication-Info']
        authResponse = self.extractVarParams(authenticationInfo)
        fromPP = authResponse['from-PP']
        return fromPP

#    function performTheLogin($username, $password, $lc){
#        $DALogin = $this->passportProps['DALogin'];
#        $authParams = array(
#            'Passport1.4 OrgVerb'=> 'GET',
#            'OrgURL'=> 'http%3A%2F%2Fmessenger%2Emsn%2Ecom',
#            'sign-in'=> $this->encode($username),
#            'pwd' => $this->encode($password),
#            'lc' => $lc
#        );
#        $authorization = $this->buildParamVars($authParams);
#        $requestParams = array(
#            'Authorization' => $authorization
#        );
#        $httpRequest = $this->buildHttpRequestHeader($DALogin, $requestParams);
#        $httpResponse = $this->request($DALogin, 443, $httpRequest);
#        $httpHeader = $this->extractHttpResponseHeader($httpResponse);
#        $authenticationInfo = $httpHeader['Authentication-Info'];
#        $authResponse = $this->extractVarParams($authenticationInfo);
#        $fromPP = $authResponse['from-PP'];
#        return $fromPP;
#    }

    def authenticate(self, username, password, lc):
        self.connectToTheNexus()
        token = self.performTheLogin(username, password, lc)
        return token

#    function authenticate($username, $password, $lc){
#            $this->connectToTheNexus();
#            $token = $this->performTheLogin($username, $password, $lc);
#            $token = substr($token, 1, (strlen($token) - 2) );
#            return $token;
#    }
#}
