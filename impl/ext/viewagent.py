""" View client install. """

import requests
import os
import sys
import platform
import urlparse
import subprocess
import tempfile
import buildweb
import re

INSTALL_PARAMS = [
]


def download_viewclient_installer(product='view',branch='view15h2',buildtype='release',buildid='',kind='official'):
    """ Download the View Client installer from buildweb. """
    # XXX need to make sure ''external_version'' definitively identifies the
    # downloaded MSI.
    arch = 'x86_64' if platform.machine().endswith('64') else 'x86'
    if arch is 'x86_64':
        file_pattern = r'VMware-viewagent-%s-\w+\.\w+\.\w+\-\d+\.exe' % arch
    else:
        file_pattern = r'VMware-viewagent-\w+\.\w+\.\w+\-\d+\.exe'
    return buildweb.download_deliverable_file(
        product,
        file_pattern,
        tempfile.gettempdir(),
        branch,
        buildtype,
        buildid,
        kind)


def install(product='view',branch='view15h2',buildtype='release',buildid='',kind='official',ipversion='ipv4',rds=False,brokerIP='',brokerUsername='hovdi.qa\\administrator',brokerPassword='ca$hc0w'):
    """ Install the MSI. """
    # Now download the latest view agent build
    installer_path = download_viewclient_installer(product,branch,buildtype,buildid,kind)
    
    # run the installer
    print ">>> Starting viewclient installer"
    #
    # XXX MSI's /v option is a double-quoted string to be fed literally to the
    # installer. As such, there's no shell expansion. Any double quotes must be
    # doubled (but not tripled, or quadrupled).
    # So for example, the double quote noted below CANNOT be adjacent to the previous
    # closing double quote, because that would have formed a triple quote.
    #                                                       V
    #msi_v_args = '"/qn /l* ""%s"" REBOOT=""ReallySuppress"" "' % \
    #             os.path.join(os.path.dirname(installer_path), 'viewclient-inst.log')
    # ADDLOCAL=VmVideo,RTAV,SVIAgent,ScannerRedirection,SerialPortRedirection,SmartCard,TSMMR,ThinPrint,USB,V4V,VPA,VmwVaudio,RDP,Core,BlastProtocol,ClientDriveRedirection,PCoIP,UnityTouch,FLASHMMR

    if ipversion == 'ipv6':
        IP_Protocol = 'IPv6'
    else:
        IP_Protocol = 'IPv4'

    import socket
    domain_name = socket.getfqdn().replace(socket.gethostname()+'.', '')
    broker_username = domain_name + '\\' + 'administrator'
    if ipversion == 'ipv6':
        selected_components = 'Core,PCoIP,BlastProtocol,RDP,ThinPrint,USB'
    else:
        #selected_components = 'VmVideo,RTAV,ScannerRedirection,SerialPortRedirection,SmartCard,TSMMR,ThinPrint,USB,V4V,VPA,VmwVaudio,RDP,Core,BlastProtocol,ClientDriveRedirection,PCoIP,UnityTouch,FLASHMMR'
        #selected_components = 'VmVideo,RTAV,ScannerRedirection,SerialPortRedirection,SmartCard,TSMMR,ThinPrint,USB,V4V,VPA,VmwVaudio,RDP,Core,ClientDriveRedirection,FLASHMMR'
        selected_components = 'ALL'
    if rds:
        msi_v_args = '"/qn ADDLOCAL=%s VDM_SERVER_NAME=%s VDM_SERVER_USERNAME=%s VDM_SERVER_PASSWORD=%s VDM_IP_PROTOCOL_USAGE=%s REBOOT=""ReallySuppress"" "' % (selected_components,brokerIP,broker_username,brokerPassword,IP_Protocol)
    else:
        msi_v_args = '"/qn ADDLOCAL=%s VDM_IP_PROTOCOL_USAGE=%s REBOOT=""ReallySuppress"" "' % (selected_components, IP_Protocol)

    cmd_and_args = [
        installer_path,
        '/s', # MSI slient install
        '/v', # MSI /v option
        msi_v_args]
    print 'Starting subprocess:\n    %s' % (' '.join(cmd_and_args))
    try:
        subprocess.check_call(' '.join(cmd_and_args), shell=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 3010:
            # install success (3010 means success but needs reboot)
            print "Successfully installed view agent, pending reboot"
        else:
            print "Installation failed with error code %d" % e.returncode
            raise
    print "NeedsReboot"

def view_agent_installed():
    try:
        output = subprocess.check_output('wmic product get name | find "Horizon Agent"',shell=True)
        if "Horizon Agent" in output:
            return True
        else:
            return False
    except:
        return False

def get_installed_id():
    output = subprocess.check_output('wmic product get IdentifyingNumber,name |find "Horizon Agent"',shell=True)
    if "Horizon Agent" in output:
        return output.split(' ')[0]


def uninstall():
    if view_agent_installed():
        installed_id = get_installed_id()
        subprocess.call('msiexec /norestart /q/x%s REMOVE=ALL' % installed_id,shell=True)


def get_build_version():
    try:
        output = subprocess.check_output('wmic product get name,version,installdate | find "Horizon Agent"',shell=True)
        if "Horizon Agent" in output:
            version = output.strip().split(' ')[-1]
            installdate = output.strip().split(' ')[0]
            return version, installdate
        else:
            return 'NA', 'NA'
    except:
        return 'NA', 'NA'


if __name__ == '__main__':
    install()
    pass
