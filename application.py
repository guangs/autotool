# ===============================================================================
# description     :All API interfaces this program can provide to external program
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/23
# python version  :2.7
# ===============================================================================

import os,common,webclient,time
import conf.loggingproperties as logging_properties
from conf.config import *
import threading


PORT = 9180
Log_Transfer_PORT = 9280
print locals().keys()
if locals().has_key("ClientHost"):
    CLIENT_HOSTS = ClientHost
else:
    CLIENT_HOSTS = []

if locals().has_key("AgentHost"):
    AGENT_HOSTS = AgentHost
else:
    AGENT_HOSTS = []

if isinstance(CLIENT_HOSTS,str):
    CLIENT_HOSTS = [CLIENT_HOSTS]
if isinstance(AGENT_HOSTS,str):
    AGENT_HOSTS = [AGENT_HOSTS]

class MyThread(threading.Thread):
    def __init__(self,target=None,args=None):
        super(MyThread, self).__init__()
        self.exitcode = 0
        self.exception = None
        self.target = target
        self.args = args

    def run(self):
        try:
            if self.target:
                self.target(*self.args)
        except webclient.CaptureLogException,e:
            self.exitcode = 1
            self.exception = e

def enable_dct_logs():
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.DCTLogEnabled['client'])
    for key,name,value,type in temp_parser.parse():
        for CLIENT_HOST in CLIENT_HOSTS:
            webclient.setRegistryValue(key,name,value,type,CLIENT_HOST+':'+str(PORT))
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.DCTLogEnabled['agent'])
    for key,name,value,type in temp_parser.parse():
        for AGENT_HOST in AGENT_HOSTS:
            webclient.setRegistryValue(key,name,value,type,AGENT_HOST+':'+str(PORT))
    print 'Enable DCT logs successfully'

def disable_dct_logs():
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.DCTLogEnabled['client'])
    for key,name,value,type in temp_parser.parse():
        for CLIENT_HOST in CLIENT_HOSTS:
            webclient.delRegistryValue(key,name,CLIENT_HOST+':'+str(PORT))
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.DCTLogEnabled['agent'])
    for key,name,value,type in temp_parser.parse():
        for AGENT_HOST in AGENT_HOSTS:
            webclient.delRegistryValue(key,name,AGENT_HOST+':'+str(PORT))
    print 'Disable DCT logs successfully'

def enable_thinprint_logs():
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.ThinPrintLogEnabled['client'])
    for key,name,value,type in temp_parser.parse():
        for CLIENT_HOST in CLIENT_HOSTS:
            webclient.setRegistryValue(key,name,value,type,CLIENT_HOST+':'+str(PORT))
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.ThinPrintLogEnabled['agent'])
    for key,name,value,type in temp_parser.parse():
        for AGENT_HOST in AGENT_HOSTS:
            webclient.setRegistryValue(key,name,value,type,AGENT_HOST+':'+str(PORT))
    print 'Enable ThinPrint logs successfully'

def disable_thinprint_logs():
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.ThinPrintLogEnabled['client'])
    for key,name,value,type in temp_parser.parse():
        for CLIENT_HOST in CLIENT_HOSTS:
            webclient.delRegistryValue(key,name,CLIENT_HOST+':'+str(PORT))
    temp_parser = common.RegistryMultipleFilesParser(logging_properties.ThinPrintLogEnabled['agent'])
    for key,name,value,type in temp_parser.parse():
        for AGENT_HOST in AGENT_HOSTS:
            webclient.delRegistryValue(key,name,AGENT_HOST+':'+str(PORT))
    print 'Disable ThinPrint logs successfully'

def enable_configured_logs():
    'not finish yet'
    pass

def start_capture_logs():
    client_log_dirs = logging_properties.LogDirs['client']
    agent_log_dirs = logging_properties.LogDirs['agent']
    filefilter = r'.*'
    dst_dir = 'C:\\vdm-sdct-auto'
    threads = []
    thread_exception_flag = False
    thread_exception_info = ''

    for CLIENT_HOST in CLIENT_HOSTS:
        for log_dir in client_log_dirs:
            t = MyThread(target=webclient.startCaptureLog,args=(log_dir,filefilter,dst_dir,5,300,CLIENT_HOST+':'+str(PORT),200))
            t.setDaemon(True)
            t.start()
            threads.append(t)
            time.sleep(0.2)
            # webclient.startCaptureLog(log_dir,filefilter,dst_dir,5,300,CLIENT_HOST+':'+str(PORT),200)
    for AGENT_HOST in AGENT_HOSTS:
        for log_dir in agent_log_dirs:
            t = MyThread(target=webclient.startCaptureLog,args=(log_dir,filefilter,dst_dir,5,300,AGENT_HOST+':'+str(PORT),200))
            t.setDaemon(True)
            t.start()
            threads.append(t)
            time.sleep(0.2)
            # webclient.startCaptureLog(log_dir,filefilter,dst_dir,5,300,AGENT_HOST+':'+str(PORT),200)
    for t in threads:
        t.join()
        if t.exitcode != 0:
            thread_exception_flag = True
            thread_exception_info = t.exception.value

    if thread_exception_flag:
        print 'start capture logs failed with description<' + thread_exception_info + '>, please retry'
    else:
        print 'start capture logs successfully'

def stop_capture_logs():
    client_log_dirs = logging_properties.LogDirs['client']
    agent_log_dirs = logging_properties.LogDirs['agent']
    if locals().has_key("SaveLogsDirectory"):
        local_savelog_root_dir = SaveLogsDirectory
    else:
        local_savelog_root_dir = 'C:\\Users\\Administrator\\Desktop\\vdm-sdct-auto'
    local_savelog_sub_dir = os.path.join(local_savelog_root_dir,time.strftime('%Y%m%d%H%M%S'))
    filefilter = r'.*'
    dst_dir = 'C:\\vdm-sdct-auto'
    try:
        for CLIENT_HOST in CLIENT_HOSTS:
            for log_dir in client_log_dirs:
                webclient.stopCaptureLog(log_dir,filefilter,dst_dir,CLIENT_HOST+':'+str(PORT),200)
            webclient.zipLogs(dst_dir,CLIENT_HOST+':'+str(PORT),200)
            local_savelog_sub_dir_client = os.path.join(local_savelog_sub_dir,'client' + '(' + CLIENT_HOST + ')')
            if not os.path.exists(local_savelog_sub_dir_client):
                os.makedirs(local_savelog_sub_dir_client)
            webclient.getZipLogs(local_savelog_sub_dir_client,dst_dir,CLIENT_HOST,Log_Transfer_PORT)
        for AGENT_HOST in AGENT_HOSTS:
            for log_dir in agent_log_dirs:
                webclient.stopCaptureLog(log_dir,filefilter,dst_dir,AGENT_HOST+':'+str(PORT),200)
            webclient.zipLogs(dst_dir,AGENT_HOST+':'+str(PORT),200)
            local_savelog_sub_dir_agent = os.path.join(local_savelog_sub_dir,'agent' + '(' + AGENT_HOST + ')')
            if not os.path.exists(local_savelog_sub_dir_agent):
                os.makedirs(local_savelog_sub_dir_agent)
            webclient.getZipLogs(local_savelog_sub_dir_agent,dst_dir,AGENT_HOST,Log_Transfer_PORT)
        print 'stop capture logs successfully'
    except webclient.CaptureLogException,e:
        print 'stop capture logs failed with description<' + e.value + '>, please retry'


if __name__ == '__main__':
    enable_configured_logs()
