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

urls = ('/rest/registry/?', 'RegistryService',
        '/rest/logging','LoggingService',
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

def start_web_services():
    # start log transfer server in sub thread
    logtransfer.start_server()
    # start all web services in main thread
    app = web.application(urls, globals())
    app.run()

def create_tempdir():
    if not os.path.exists('C:\\Temp'):
        os.makedirs('C:\\Temp')

if __name__ == "__main__":
    create_tempdir()
    start_web_services()