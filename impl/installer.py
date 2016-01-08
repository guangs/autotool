# =====================================================================================
# description     :It is the implementation to install/reinstall/uninstall view for web service
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.2
# date            :2015/11/26
# python version  :2.7
# =====================================================================================
import os
from ext import *
import windows
import platform
import threading

class InstallException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def agent_reinstall(branch,buildid,latest,kind,buildtype,ipversion,rds,broker):
    if not os.path.exists('C:\\Temp\\reboot_after_tasks.txt'):
        with open('C:\\Temp\\reboot_after_tasks.txt','w+') as f:
            f.write("installer.agent_install('%s','%s','%s','%s','%s','%s','%s','%s')" % (branch,buildid,latest,kind,buildtype,ipversion,rds,broker))
    else:
        with open('C:\\Temp\\reboot_after_tasks.txt','r') as f:
            pending_tasks = f.read()
        if 'agent_install' not in pending_tasks:
            with open('C:\\Temp\\reboot_after_tasks.txt','a+') as f:
                f.write("installer.agent_install('%s','%s','%s','%s','%s','%s','%s','%s')" % (branch,buildid,latest,kind,buildtype,ipversion,rds,broker))
        else:
            # there is error in last time, reset pending tasks
            with open('C:\\Temp\\reboot_after_tasks.txt','w+') as f:
                f.write("installer.agent_install('%s','%s','%s','%s','%s','%s','%s','%s')" % (branch,buildid,latest,kind,buildtype,ipversion,rds,broker))
    t = threading.Thread(target=agent_uninstall)
    t.start()


def agent_uninstall():
    if viewagent.view_agent_installed():
        viewagent.uninstall()
    #restart system
    windows.delay_reboot(10)


def agent_install(branch,buildid,latest,kind,buildtype,ipversion,rds,broker):
    #install driver certification for USB
    current_dir = os.path.abspath('.')
    base_dir = os.sep.join(current_dir.split(os.sep)[:-1])
    res_dir = os.path.join(base_dir,'res')
    view_agent_usb_cer_file = os.path.join(res_dir,'ViewAgentUSB.cer')
    # you can use certmgr.msc to check it
    os.system('certutil -addstore "TrustedPublisher" {}'.format(view_agent_usb_cer_file))
    #install new build
    if latest == 'true':
        buildid = ''
    if 'Server' in platform.release():
        viewagent.install('view',branch,buildtype,buildid,kind,ipversion,True,broker)
    else:
        viewagent.install('view',branch,buildtype,buildid,kind,ipversion)
    #restart system
    windows.delay_reboot(10)


def client_reinstall(branch,buildid,latest,kind,buildtype,ipversion):
    def reinstall(branch,buildid,latest,kind,buildtype,ipversion):
        viewclient.uninstall()
        if latest == 'true':
            buildid = ''
        viewclient.install('viewclientwin',branch,buildtype,buildid,kind,ipversion)
        #restart system
        windows.delay_reboot(5)
    t = threading.Thread(target=reinstall,args=(branch,buildid,latest,kind,buildtype,ipversion))
    t.start()

def client_install(branch,buildid,latest,kind,buildtype,ipversion):
    pass

def client_uninstall():
    pass

def broker_reinstall(branch,buildid,latest,kind,buildtype,ipversion):
    def reinstall(branch,buildid,latest,kind,buildtype,ipversion):
        #uninstall existing build
        viewbroker.uninstall()
        #install new build
        if latest == 'true':
            buildid = ''
        viewbroker.install('view',branch,buildtype,buildid,kind,ipversion)
        #restore automation config for broker
        os.system('C:\\autotool\\scripts\\Wincdk_BATs_config_broker.bat')
        #restart system
        windows.delay_reboot(5)
    t = threading.Thread(target=reinstall,args=(branch,buildid,latest,kind,buildtype,ipversion))
    t.start()


def broker_install(branch,buildid,latest,kind,buildtype,ipversion):
    pass


def broker_uninstall():
    pass