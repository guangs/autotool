# ===============================================================================
# description     :Misc functions and common templates used by other modules
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/23
# python version  :2.7
# ===============================================================================

import httplib
import ConfigParser
import os
import tempfile
import logging
from logging.handlers import RotatingFileHandler
import conf.config as config_file
import conf.loggingproperties as logging_properties

commonheaders = {"Content-type": "application/xml","Accept": "application/xml"}
commonheaders_json = {"Content-type": "application/json","Accept": "application/json"}
tempdir = os.getcwd() + os.sep + 'temp'
resdir = os.getcwd() + os.sep + 'res'
impldir = os.getcwd() + os.sep + 'impl'
confdir = os.getcwd() + os.sep + 'conf'
LOG_FILE = tempdir + os.sep + 'autotool.log'
rfile_handler = RotatingFileHandler(LOG_FILE,maxBytes=1024*1024,backupCount=3)
logger = logging.getLogger('autotool')
logger.addHandler(rfile_handler)
logger.setLevel(logging.DEBUG)

def GetMessage(site,url,json=True):
    data=''
    conn=None
    FirstPass=False
    host = site[0]
    port = site[1]
    try:
        conn = httplib.HTTPConnection(host,port,timeout=15)
        if json:
            conn.request("GET", url, '', commonheaders_json)
        else:
            conn.request("GET", url, '', commonheaders)
        response = conn.getresponse()
        data = response.read()
        data=data.strip()
        logger.debug("\n\nthis response in GetMessage is \n %s \n" % data)
        conn.close();
        conn=None
        FirstPass=True
    except Exception as temp_exp:
        logger.debug("Get an exception when trying to connection to host and send GET "+url)
        logger.debug("Exception:"+str(temp_exp))
        logger.debug("retry it again")
        if conn:
            conn.close()
            conn=None
    try:
        if FirstPass==False:
            conn = httplib.HTTPConnection(host,port,timeout=15)
            if json:
                conn.request("GET", url, '', commonheaders_json)
            else:
                conn.request("GET", url, '', commonheaders)
            response = conn.getresponse()
            data = response.read()
            data=data.strip()
            conn.close();
        resdata={}
        resdata['ResponseStatus'] = response.status
        resdata['ResponseHeaders']=response.getheaders()
        resdata['ResponseBody'] = eval(data)
        resdata['_RAW_RES_DATA_']=data
        return resdata
    except Exception as temp_exp:
        if conn!=None:
            conn.close()

def PostMessage(site,url,body,json=True, contentType=None, AcceptTypes=None):
    data=''
    conn=None
    FirstPass=False
    host = site[0]
    port = site[1]
    resdata = {}
    try:
        conn = httplib.HTTPConnection(host,port,timeout=15)

        tempheaders=commonheaders_json
        if not json:
            tempheaders=commonheaders

        if contentType is not None:
            tempheaders["Content-type"]="application/"+contentType
        if AcceptTypes is not None:
            if len(AcceptTypes) == 0:
                del tempheaders["Accept"]
            else:
                tempheaders["Accept"]=','.join(['application/'+typeitem["name"]+"; "+typeitem["params"] for typeitem in AcceptTypes])
                if AcceptTypes[0]["name"].lower() == 'json':
                    json=True
        if url.find("resFormat=json") != -1:
            json=True
        logger.debug("\n\nthis message request in PostMessage is: \n%s\n%s\n" %(tempheaders,body))
        conn.request("POST", url, body, tempheaders)
        response = conn.getresponse()
        data = response.read()
        data=data.strip()
        logger.debug("\n\nthis response in PostMessage is \n%s \n" % data)
        conn.close()
        conn=None
        FirstPass=True
    except Exception as temp_exp:
        logger.debug("Get an exception when trying to connection to host and send GET "+url)
        logger.debug("Exception:"+str(temp_exp))
        logger.debug("retry it again")
        if conn:
            conn.close()
            conn=None

    try:
        if not FirstPass:
            conn = httplib.HTTPConnection(host,port,timeout=15)
            conn.request("POST", url, body, tempheaders)
            response = conn.getresponse()
            data = response.read()
            data=data.strip()
            conn.close()
        resdata['ResponseStatus'] = response.status
        resdata['ResponseHeaders']=response.getheaders()
        resdata['ResponseBody'] = eval(data)
        resdata['_RAW_RES_DATA_']=data
        return resdata
    except Exception as temp_exp:
        if conn!=None:
            conn.close()

def DeleteMessage(site,url,json=True):
    logger.debug("\n\nthis message url in DeleteMessage is: \n %s" % url)
    data=''
    conn=None
    FirstPass=False
    host = site[0]
    port = site[1]
    try:
        conn = httplib.HTTPConnection(host,port,timeout=15)
        tempheaders=commonheaders_json
        if not json:
            tempheaders=commonheaders
        conn.request("DELETE", url, '', tempheaders)
        response = conn.getresponse()
        data = response.read()
        logger.debug("\n\nthis response in DeleteMessage is \n %s \n" % data)
        conn.close()
        conn=None
        FirstPass=True
    except Exception as temp_exp:
        logger.debug("Get an exception when trying to connection to host and send GET "+url)
        logger.debug("Exception:"+str(temp_exp))
        logger.debug("retry it again")
        if conn:
            conn.close()
            conn=None
    try:
        if FirstPass==False:
            conn = httplib.HTTPConnection(host,port,timeout=15)
            tempheaders=commonheaders_json
            if not json:
                tempheaders=commonheaders
            conn.request("DELETE", url, '', tempheaders)
            response = conn.getresponse()
            data = response.read()
            data.strip()
            conn.close();

        resdata={}
        resdata['ResponseStatus'] = response.status
        resdata['ResponseHeaders']=response.getheaders()
        resdata['ResponseBody'] = eval(data)
        resdata['_RAW_RES_DATA_']=data
        return resdata
    except Exception as temp_exp:
        if conn!=None:
            conn.close()

class RegistryParser:
    def __init__(self):
        pass
    def parser(self):
        pass

class RegistrySingleFileParser(RegistryParser):

    def __init__(self,registry_filename):
        self.registry_filename = registry_filename

    def _read_reg(self,filename):
        with open(filename,'r') as f:
            content = f.readlines()
        return ''.join(content[1:])

    def _load_file(self):
        global tempdir
        global resdir
        temp = tempdir + os.sep + 'single_registry_file.txt'
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
        with open(temp,'w+') as tf:
            reg_file = resdir+ os.sep + self.registry_filename
            contents = self._read_reg(reg_file)
            tf.write(contents)
        conf = ConfigParser.ConfigParser()
        conf.optionxform = str
        conf.read(tf.name)
        return conf

    def parse(self):

        def get_name(raw_registry_name):
            'remove first " and last "'
            return raw_registry_name[1:-1]

        def get_value(raw_registry_value):
            if ':' not in raw_registry_value:
                return raw_registry_value[1:-1]
            if raw_registry_value.startswith('dword:'):
                from_index = raw_registry_value.index('dword:') + 6
                return int(raw_registry_value[from_index:],16)
            elif raw_registry_value.startswith('hex:'):
                pass
            elif raw_registry_value.startswith('hex(b):'):
                pass
            elif raw_registry_value.startswith('hex(7):'):
                pass
            elif raw_registry_value.startswith('hex(2):'):
                pass
            else:
                return raw_registry_value[1:-1]

        def get_type(raw_registry_value):
            if ':' not in raw_registry_value:
                return 'REG_SZ'
            if raw_registry_value.startswith('dword:'):
                return 'REG_DWORD'
            elif raw_registry_value.startswith('hex:'):
                return 'REG_BINARY'
            elif raw_registry_value.startswith('hex(b):'):
                return 'REG_DWORD_BIG_ENDIAN'
            elif raw_registry_value.startswith('hex(7):'):
                return 'REG_MULTI_SZ'
            elif raw_registry_value.startswith('hex(2):'):
                return 'REG_EXPAND_SZ'
            else:
                return 'REG_SZ'

        registry_config = []
        conf = self._load_file()
        for sec in conf.sections():
            for each in conf.items(sec):
                key = sec
                name = get_name(each[0])
                value = get_value(each[1])
                type = get_type(each[1])
                registry_config.append((key,name,value,type))
        return registry_config


class RegistryMultipleFilesParser(RegistryParser):

    def __init__(self,registry_file_list):
        self.registry_file_list = registry_file_list

    def parse(self):
        registry_config = []
        for reg in self.registry_file_list:
            temp_parser = RegistrySingleFileParser(reg)
            temp_content = temp_parser.parse()
            registry_config.extend(temp_content)
        return registry_config

class RegistryDirFilesParser(RegistryParser):

    def __init__(self,registry_dirname = os.getcwd() + os.sep + 'res'):
        self.registry_dirname = registry_dirname

    def parse(self):
        dirname = self.registry_dirname
        files = filter(lambda f: f[-4:]=='.reg',os.listdir(dirname))
        temp_parser = RegistryMultipleFilesParser(files)
        temp_content = temp_parser.parse()
        return temp_content

# class Configuration(object):
#
#     config = {}
#
#     def __init__(self):
#         pass
#
#     def __new__(cls,*args,**kwargs):
#         if cls.config == {}:
#             cls._load_file()
#         return cls.config
#
#     @classmethod
#     def _load_file(cls,config_file_name=None):
#         if config_file_name is None:
#             'import config from configuration'
#             cls._parse_registry_conf()
#             cls._parse_other_conf()
#         else:
#             'import config from other config'
#
#     @classmethod
#     def _parse_registry_conf(cls):
#         enabled_reg_names_client = []
#         enabled_reg_names_agent = []
#         if config_file.ThinPrintLogEnabled:
#             enabled_reg_names_client.extend(logging_properties.ThinPrintLogEnabled['client'])
#             enabled_reg_names_agent.extend(logging_properties.ThinPrintLogEnabled['agent'])
#             temp_parser = RegistryMultipleFilesParser(enabled_reg_names_client)
#             cls.config['client_log_flags'] = temp_parser.parse()
#             temp_parser = RegistryMultipleFilesParser(enabled_reg_names_agent)
#             cls.config['agent_log_flags'] = temp_parser.parse()
#         'not finish yet'
#
#     @classmethod
#     def _parse_other_conf(cls):
#         'reserved for future'
#         cls.config['general'] = {}
#         if config_file.ViewAgentHost is not None:
#             cls.config['general']['ViewAgentHost']=config_file.ViewAgentHost
#
#
# class DataBase:
#     pass

if __name__ == '__main__':
    'To be tested'
    conf = Configuration()
    print conf


