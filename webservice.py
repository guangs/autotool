# =====================================================================================
# description     :REST web service based on json message, it call impl module
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/16
# python version  :2.7
# =====================================================================================

import web
import json
import re
import os
import urllib
from impl import *
import threading
import impl.ext.viewagent as viewagent
import impl.ext.viewclient as viewclient
import impl.ext.viewbroker as viewbroker

urls = ('/rest/registry/?', 'RegistryService',
        '/rest/logging','LoggingService',
        '/rest/cmd','CommandService',
        '/rest/install','InstallService',
        '/rest/buildinfo','BuildInfoService'
       )
SetRegistryResponseJSON = '{"registry":{"status":"OK"}}'
SetRegistryResponseJSON_Error = '{"registry":{"status":"Error"}}'

StartLoggingResponseJSON = '{"startloggingresponse":{"status":"OK"}}'
StartLoggingResponseJSON_Error = '''{
  "startloggingresponse": {
    "status": "Error",
    "description": "%s"
  }
}'''

StopLoggingResponseJSON = '{"stoploggingresponse":{"status":"OK"}}'
StopLoggingResponseJSON_Error = '''{
  "stoploggingresponse": {
    "status": "Error",
    "description": "%s"
  }
}'''

ZipLogsResponseJSON = '{"ziplogsresponse":{"status":"OK"}}'
ZipLogsResponseJSON_Error = '''{
  "ziplogsresponse": {
    "status": "Error",
    "description": "%s"
  }
}'''

LoggingResponseJSON_Error = '{"loggingresponse":{"status":"Error"}}'
LoggingResponseJSON_NotSupport = '{"loggingresponse":{"status":"Not Support Request"}}'

CommandResponseJSON = '{"response":{"status":"OK"}}'
CommandResponseJSON_Error = '''{
  "response": {
    "status": "Error",
    "description": "%s"
  }
}'''

InstallResponseJSON = '{"response":{"status":"OK"}}'
InstallResponseJSON_Error = '''{
  "response": {
    "status": "Error",
    "description": "%s"
  }
}'''

BuildInfoResponseJSON = '''{
  "response": {
    "role": "%s",
    "build_version": "%s",
    "build_installdate": "%s",
    "status": "OK"
  }
}'''

BuildInfoResponseJSON_Error = '''{
  "response": {
    "status": "Error",
    "description": "%s"
  }
}'''


buildinfo = {'client': 'NA', 'agent': 'NA', 'broker': 'NA'}

class RegistryService(object):
    def GET(self):
        try:
            queryprams = web.input()
            web.header('Content-Type', 'application/json')
            reg = registry.Registry()
            key = queryprams.key
            name = queryprams.name
            val = reg.get_value(key, name)
            retstr = json.dumps(val)
            web.header('Content-Length', len(retstr))
            return retstr
        except AttributeError:
            print 'there is error'
            val = None
            return json.dumps(val)

    def POST(self):
        try:
            web.header('Content-Type', 'application/json')
            body = web.data().strip()
            print body
            msgobj = eval(body)['registry']
            key = msgobj['key']
            name = msgobj['name']
            value = msgobj['value']
            type = msgobj['type']
            reg = registry.Registry()
            print "key,name,value,type is\n%s\n%s\n%s\n%s" % (key,name,value,type)
            success = reg.set_value(key, name, value, type)
            print success
            retstr = ''
            if success:
                retstr = SetRegistryResponseJSON
            else:
                retstr = SetRegistryResponseJSON_Error
            web.header('Content-Length', len(retstr))
            return retstr
        except AttributeError:
            print 'there is error'
            val = False
            return json.dumps(val)

    def DELETE(self):
        try:
            queryprams = web.input()
            web.header('Content-Type', 'application/json')
            reg = registry.Registry()
            key = urllib.unquote(queryprams.key)
            name = urllib.unquote(queryprams.name)
            success = reg.del_value(key, name)
            print success
            retstr = ''
            if success:
                retstr = SetRegistryResponseJSON
            else:
                retstr = SetRegistryResponseJSON_Error
            web.header('Content-Length', len(retstr))
            return retstr
        except AttributeError:
            print 'there is error'
            val = False
            return json.dumps(val)

class LoggingService(object):

    def POST(self):
        try:
            web.header('Content-Type', 'application/json')
            body = web.data().strip()
            print body
            msgobj = eval(body)
            if 'startloggingrequest' in msgobj.keys():
                try:
                    self.handle_startloggingrequest(msgobj)
                    return StartLoggingResponseJSON
                except logcaptor.LogCaptorException, e:
                    return StartLoggingResponseJSON_Error % e.value
            elif 'stoploggingrequest' in msgobj.keys():
                try:
                    self.handle_stoploggingrequest(msgobj)
                    return StopLoggingResponseJSON
                except logcaptor.LogCaptorException, e:
                    return StopLoggingResponseJSON_Error % e.value
            elif 'ziplogsrequest' in msgobj.keys():
                try:
                    self.handle_ziplogsrequest(msgobj)
                    return ZipLogsResponseJSON
                except logcaptor.LogCaptorException, e:
                    return ZipLogsResponseJSON_Error % e.value
            else:
                'not support'
                return LoggingResponseJSON_NotSupport
        except AttributeError:
            print 'there is error'
            return LoggingResponseJSON_Error

    def handle_startloggingrequest(self,msgobj):
        request = msgobj['startloggingrequest']
        srcdir = request['srcdir']['name']
        filefilter = request['srcdir']['filefilter']
        if filefilter == '' or None:
            filefilter = r'.*'
        dstdir = request['dstdir']
        interval = request['interval']
        timeout = request['timeout']
        lc = logcaptor.LogCaptor(srcdir,filefilter)
        lc.start()

    def handle_stoploggingrequest(self,msgobj):
        request = msgobj['stoploggingrequest']
        srcdir = request['srcdir']['name']
        filefilter = request['srcdir']['filefilter']
        dstdir = request['dstdir']
        dstdir = logcaptor.LogCaptor._replace_username(dstdir)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        lc = logcaptor.LogCaptor(srcdir,filefilter)
        lc.stop(dstdir)


    def handle_ziplogsrequest(self,msgobj):
        request = msgobj['ziplogsrequest']
        dstdir = logcaptor.LogCaptor._replace_username(request['dstdir'])
        logcaptor.LogCaptor.zip_logs(dstdir)


class CommandService(object):

    def POST(self):
        try:
            web.header('Content-Type', 'application/json')
            body = web.data().strip()
            print body
            msgobj = eval(body)
            if 'request' in msgobj.keys():
                try:
                    request = msgobj['request']
                    command = request['command']
                    interpreter = request['interpreter']
                    role = request['role']
                    cmdexecutor.execute(command,interpreter,role)
                    return CommandResponseJSON
                except cmdexcutor.CommandException,e:
                    return CommandResponseJSON_Error % e.value
            else:
                'not support'
                return CommandResponseJSON_Error % 'not support'
        except AttributeError:
            print 'there is error'
            return CommandResponseJSON_Error % 'there is AttributeError'

class InstallService(object):

    def POST(self):
        try:
            web.header('Content-Type', 'application/json')
            body = web.data().strip()
            print body
            msgobj = eval(body)
            if 'request' in msgobj.keys():
                try:
                    request = msgobj['request']
                    installtype = request['installtype']
                    installrole = request['installrole']
                    branch = request['branch']
                    buildid = request['buildid']
                    latest = request['latest']
                    kind = request['kind']
                    buildtype = request['buildtype']
                    ipversion = request['ipversion']
                    rds = request['rds']
                    broker = request['broker']
                    if installtype == 'reinstall':
                        if installrole == 'agent':
                            installer.agent_reinstall(branch,buildid,latest,kind,buildtype,ipversion,rds,broker)
                        elif installrole == 'client':
                            installer.client_reinstall(branch,buildid,latest,kind,buildtype,ipversion)
                        else:
                            installer.broker_reinstall(branch,buildid,latest,kind,buildtype,ipversion)
                    elif installtype == 'install':
                        if installrole == 'agent':
                            installer.agent_install(branch,buildid,latest,kind,buildtype,ipversion,rds,broker)
                        elif installrole == 'client':
                            installer.client_install(branch,buildid,latest,kind,buildtype,ipversion)
                        else:
                            installer.broker_install(branch,buildid,latest,kind,buildtype,ipversion)
                    elif installtype == 'uninstall':
                        if installrole == 'agent':
                            installer.agent_uninstall()
                        elif installrole == 'client':
                            installer.client_uninstall()
                        else:
                            installer.broker_uninstall()
                    else:
                        return InstallResponseJSON_Error % 'Not support install type'
                    return InstallResponseJSON
                except installer.InstallException,e:
                    return InstallResponseJSON_Error % e.value
            else:
                'not support'
                return InstallResponseJSON_Error % 'not support'
        except AttributeError:
            print 'there is error'
            return InstallResponseJSON_Error % 'there is AttributeError'


class BuildInfoService(object):

    def POST(self):
        global buildinfo
        try:
            web.header('Content-Type', 'application/json')
            body = web.data().strip()
            print body
            msgobj = eval(body)
            if 'request' in msgobj.keys():
                request = msgobj['request']
                role = request['role']
                if role == 'client':
                    if buildinfo['client'] != 'NA':
                        build_version, build_installdate = buildinfo['client']
                    else:
                        build_version, build_installdate = viewclient.get_build_version()
                        buildinfo['client'] = (build_version, build_installdate)
                    return BuildInfoResponseJSON % ('client',build_version,build_installdate)
                elif role == 'agent':
                    if buildinfo['agent'] != 'NA':
                        build_version, build_installdate = buildinfo['agent']
                    else:
                        build_version, build_installdate = viewagent.get_build_version()
                        buildinfo['agent'] = (build_version, build_installdate)
                    return BuildInfoResponseJSON % ('agent',build_version,build_installdate)
                elif role == 'broker':
                    if buildinfo['broker'] != 'NA':
                        build_version, build_installdate = buildinfo['broker']
                    else:
                        build_version, build_installdate = viewbroker.get_build_version()
                        buildinfo['broker'] = (build_version, build_installdate)
                    return BuildInfoResponseJSON % ('broker',build_version,build_installdate)
                else:
                    return BuildInfoResponseJSON_Error % 'not support role'
            else:
                return BuildInfoResponseJSON_Error % 'not support'
        except AttributeError:
            print 'there is error'
            return BuildInfoResponseJSON_Error % 'there is AttributeError'


def start_web_services():
    # start log transfer server in sub thread
    logtransfer.start_server()
    # start all web services in main thread
    app = web.application(urls, globals())
    app.run()


def handle_reboot_after_tasks():
    if not os.path.exists('C:\\Temp\\reboot_after_tasks.txt'):
        return
    with open('C:\\Temp\\reboot_after_tasks.txt', 'r') as f:
        tasks = f.readlines()
    os.remove('C:\\Temp\\reboot_after_tasks.txt')
    for task in tasks:
        exec('''%s''' % task)
    collect_build_info_after_started()


def collect_build_info_after_started():
    import webclient
    # import time
    # time.sleep(15)
    try:
        webclient.getBuildInfo('client')
    except webclient.ServiceException,e:
        print 'getting client build info failed with description<' + e.value + '>, please retry'
    try:
        webclient.getBuildInfo('broker')
    except webclient.ServiceException,e:
        print 'getting broker build info failed with description<' + e.value + '>, please retry'
    try:
        webclient.getBuildInfo('agent')
    except webclient.ServiceException,e:
        print 'getting agent build info failed with description<' + e.value + '>, please retry'


def create_tempdir():
    if not os.path.exists('C:\\Temp'):
        os.makedirs('C:\\Temp')

if __name__ == "__main__":
    create_tempdir()
    t = threading.Thread(target=handle_reboot_after_tasks)
    # t.setDaemon(True)
    t.start()
    # t2 = threading.Thread(target=collect_build_info_after_started)
    # t2.setDaemon(True)
    # t2.start()
    start_web_services()
