# =====================================================================================
# description     :http client module to call web service, invoked by application module
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/23
# python version  :2.7
# =====================================================================================

import common,socket,os
import logging
import urllib

RegistryURL = '/rest/registry'
LoggingURL = '/rest/logging'

SetRegistryRequestJSON = '''
{
  "registry":{
    "key":r"%s",
    "name":"%s",
    "value":"%s",
    "type":"%s",
  }
}'''


StartLoggingRequestJSON = '''
{
  "startloggingrequest": {
    "srcdir": {
      "name": r"%s",
      "filefilter": "%s"
    },
    "dstdir": r"%s",
    "interval": "%d",
    "timeout": "%d"
  }
}'''

StopLoggingRequestJSON = '''
{
  "stoploggingrequest": {
    "srcdir": {
      "name": r"%s",
      "filefilter": "%s"
    },
    "dstdir": r"%s"
  }
}'''

ZipLogsRequestJSON = '''
{
  "ziplogsrequest": {
    "dstdir": r"%s"
  }
}'''

logger = logging.getLogger('autotool')

class CaptureLogException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getRegistryValue(key,name,addr='localhost:9180',expectStatus =200):
    GetRegistryURL = RegistryURL + r'?key=%s&name=%s'  % (key, name)
    logger.debug(GetRegistryURL)
    site = tuple(addr.split(':'))
    res = common.GetMessage(site,GetRegistryURL)
    if not res:
        return None
    value = res['ResponseBody']
    status = res['ResponseStatus']
    if status == expectStatus:
        return value
    else:
        return None

def setRegistryValue(key,name,value,type,addr='localhost:9180',expectStatus =200):
    json_postmsg = SetRegistryRequestJSON % (key,name,value,type)
    logger.debug(json_postmsg)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,RegistryURL,json_postmsg)
    if not res:
        return False
    value = res['ResponseBody']
    status = res['ResponseStatus']
    if status == expectStatus:
        return True
    else:
        return False

def delRegistryValue(key,name,addr='localhost:9180',expectStatus =200):
    DelRegistryURL = RegistryURL + r'?key=%s&name=%s'  % (urllib.quote(key), urllib.quote(name))
    logger.debug(DelRegistryURL)
    site = tuple(addr.split(':'))
    res = common.DeleteMessage(site,DelRegistryURL)
    if not res:
        return False
    value = res['ResponseBody']
    status = res['ResponseStatus']
    if status == expectStatus:
        return True
    else:
        return False

def startCaptureLog(srcdir='C:\\Users\\Administrator\\Desktop',filefilter='.*\.txt',dstdir='C:\\Users\\Administrator\\Desktop\\dstdir',interval=5,timeout=300,addr='localhost:9180',expectStatus =200):
    json_postmsg = StartLoggingRequestJSON % (srcdir,filefilter,dstdir,interval,timeout)
    logger.debug(json_postmsg)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,LoggingURL,json_postmsg)
    if not res:
        raise CaptureLogException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['startloggingresponse']['status']
    if http_status != expectStatus:
        raise CaptureLogException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['startloggingresponse']['description']
        raise CaptureLogException(description)
    else:
        raise CaptureLogException('unknown status')


def stopCaptureLog(srcdir='C:\\Users\\Administrator\\Desktop',filefilter='.*\.txt',dstdir='C:\\Users\\Administrator\\Desktop\\dstdir',addr='localhost:9180',expectStatus =200):
    json_postmsg = StopLoggingRequestJSON % (srcdir,filefilter,dstdir)
    logger.debug(json_postmsg)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,LoggingURL,json_postmsg)
    if not res:
        raise CaptureLogException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['stoploggingresponse']['status']
    if http_status != expectStatus:
        raise CaptureLogException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['stoploggingresponse']['description']
        raise CaptureLogException(description)
    else:
        raise CaptureLogException('unknown status')

def zipLogs(dstdir,addr='localhost:9180',expectStatus =200):
    json_postmsg = ZipLogsRequestJSON % dstdir
    logger.debug(json_postmsg)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,LoggingURL,json_postmsg)
    if not res:
        raise CaptureLogException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['ziplogsresponse']['status']
    if http_status != expectStatus:
        raise CaptureLogException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['ziplogsresponse']['description']
        if description != 'no new logs':
            raise CaptureLogException(description)
    else:
        raise CaptureLogException('unknown status')

def getZipLogs(localdir='C:\\Users\\Administrator\\Desktop\\dstdir',remotedir='C:\\Users\\Administrator\\Desktop\\vdm-sdct-auto',ip='10.117.41.225',port=9091):
    sock = None
    zipfile = None
    zipfilename = ''
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((ip,port))
        sock.send('hello server, I want to get zip log')
        while True:
            response = sock.recv(1024)
            logger.debug(response)
            if response == 'tell me which dir':
                sock.send(remotedir)
            if response == 'zipfile is not existing':
                break
            if response == 'want zipfile name?':
                sock.send('yes')
                zipfilename = sock.recv(1024)
                sock.send('client ready')
            if response == 'server ready':
                if not os.path.exists(localdir):
                    os.mkdir(localdir)
                zipfile = open(os.path.join(localdir,zipfilename + '.zip'),'wb')
                sock.send('go!')
                while True:
                    data = sock.recv(4096)
                    if data == '_END_!!!':
                        logger.debug('receive zip file successfully')
                        break
                    zipfile.write(data)
                break
    finally:
        if zipfile:
            zipfile.close()
        if sock:
            sock.close()

if __name__ == '__main__':
    'to test it'
    #getRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb')
    #setRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb2','http://buildweb.eng.vmware.com','REG_SZ')
    #delRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb2')