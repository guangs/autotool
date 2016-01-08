# =====================================================================================
# description     :http client module to call web service, invoked by application module
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/23
# python version  :2.7
# =====================================================================================
#
import common,socket,os
import logging
import urllib
import conf.installationproperties as installationproperties
import conf.config as config

RegistryURL = '/rest/registry'
LoggingURL = '/rest/logging'
CmdURL = '/rest/cmd'
InstallURL = '/rest/install'

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

CommandRequestJSON = '''{
  "request": {
    "command": r"%s",
    "interpreter": "%s",
    "role": "%s"
  }
}'''

# installtype: reinstall,install,uninstall
InstallRequestJSON = '''{
    "request": {
        "installtype": "%s",
        "installrole": "%s",
        "branch": "%s",
        "buildid": "%s",
        "latest": "%s",
        "kind": "%s",
        "buildtype": "%s",
        "ipversion": "%s",
        "rds": "%s",
        "broker": "%s"
    }
}'''

logger = logging.getLogger('autotool')


class CaptureLogException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ServiceException(Exception):
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
        if sock:
            sock.close()
        if zipfile:
            zipfile.close()



def enableBlastUDP(role_name,addr='localhost:9180',expectStatus =200):
    json_postmsg = CommandRequestJSON % ('enable_blast_udp', 'program', role_name)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,CmdURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')


def enableBlastTCP(role_name,addr='localhost:9180',expectStatus =200):
    json_postmsg = CommandRequestJSON % ('enable_blast_tcp', 'program', role_name)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,CmdURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')

def upgradeAutotool(addr='localhost:9180',expectStatus =200,role_name='view_client'):
    bat_command = r"net use y: \\10.117.47.199\exchange\gshi /user:sanya\gshi vmware;ping 127.0.0.1 -n 10;y:\automation\autotool\dispatch.bat;net use /delete y:;ping 127.0.0.1 -n 10"
    json_postmsg = CommandRequestJSON % (bat_command, 'bat', role_name)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,CmdURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')

def rebootMachine(addr='localhost:9180',expectStatus =200,role_name='view_client'):
    bat_command = r"shutdown -r -t 5"
    json_postmsg = CommandRequestJSON % (bat_command, 'bat', role_name)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,CmdURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')

def reinstallAgent(addr='localhost:9180',expectStatus =200):
    branch = installationproperties.agent_branch
    buildid = installationproperties.agent_buildid
    latest = installationproperties.agent_latest
    kind = installationproperties.agent_kind
    buildtype = installationproperties.agent_buildtype
    ipversion = installationproperties.agent_ipversion
    rds = 'false'
    if isinstance(config.ViewBrokerHost,str):
        broker = config.ViewBrokerHost
    else: # for broker list
        broker = config.ViewBrokerHost[0]
    json_postmsg = InstallRequestJSON % ('reinstall', 'agent', branch, buildid, latest, kind, buildtype, ipversion, rds, broker)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,InstallURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')


def reinstallClient(addr='localhost:9180',expectStatus =200):
    branch = installationproperties.client_branch
    buildid = installationproperties.client_buildid
    latest = installationproperties.client_latest
    kind = installationproperties.client_kind
    buildtype = installationproperties.client_buildtype
    ipversion = installationproperties.client_ipversion
    rds = ''
    broker = config.ViewBrokerHost
    json_postmsg = InstallRequestJSON % ('reinstall', 'client', branch, buildid, latest, kind, buildtype, ipversion, rds, broker)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,InstallURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')


def reinstallBroker(addr='localhost:9180',expectStatus =200):
    branch = installationproperties.agent_branch
    buildid = installationproperties.agent_buildid
    latest = installationproperties.agent_latest
    kind = installationproperties.agent_kind
    buildtype = installationproperties.agent_buildtype
    ipversion = installationproperties.agent_ipversion
    rds = ''
    broker = config.ViewBrokerHost
    json_postmsg = InstallRequestJSON % ('reinstall', 'broker', branch, buildid, latest, kind, buildtype, ipversion, rds, broker)
    site = tuple(addr.split(':'))
    res = common.PostMessage(site,InstallURL,json_postmsg)
    if not res:
        raise ServiceException('no response')
    value = res['ResponseBody']
    http_status = res['ResponseStatus']
    status = value['response']['status']
    if http_status != expectStatus:
        raise ServiceException('error http status code')
    if status == 'OK':
        pass
    elif status == 'Error':
        description = value['response']['description']
        raise ServiceException(description)
    else:
        raise ServiceException('unknown status')

if __name__ == '__main__':
    'to test it'
    #getRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb')
    #setRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb2','http://buildweb.eng.vmware.com','REG_SZ')
    #delRegistryValue(r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp','buildweb2')