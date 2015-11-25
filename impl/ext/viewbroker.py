""" View client install. """

import requests
import os
import sys
import platform
import urlparse
import subprocess
import tempfile
import buildweb


INSTALL_PARAMS = [
]


def download_viewclient_installer(product='view',branch='view15h2',buildtype='release',buildid='',kind='official'):
    """ Download the View Client installer from buildweb. """
    # XXX need to make sure ''external_version'' definitively identifies the
    # downloaded MSI.
    arch = 'x86_64' if platform.machine().endswith('64') else 'x86'
    file_pattern = r'VMware-viewconnectionserver-%s-\w.\w.\w-\d+\.exe' % arch
    return buildweb.download_deliverable_file(
        product,
        file_pattern,
        tempfile.gettempdir(),
        branch,
        buildtype,
        buildid,
        kind)


def install(product='view',branch='view15h2',buildtype='release',buildid='',kind='official',ipversion='ipv4'):
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
    if ipversion == 'ipv6':
        IP_Protocol = 'IPv6'
    else:
        IP_Protocol = 'IPv4'
    #msi_v_args = '"/qn VDM_SERVER_INSTANCE_TYPE=1 FWCHOICE=1 HTMLACCESS=1 VDM_IP_PROTOCOL_USAGE=IPv4 VDM_INITIAL_ADMIN_SID=S-1-5-21-3011279443-1087069590-2703737120-500 VDM_SERVER_RECOVERY_PWD=ca$hc0w VDM_SERVER_RECOVERY_PWD_REMINDER=""ca$hc0w"" "'
    msi_v_args = '"/qn VDM_SERVER_INSTANCE_TYPE=1 FWCHOICE=1 HTMLACCESS=1 VDM_IP_PROTOCOL_USAGE=%s VDM_INITIAL_ADMIN_SID=S-1-5-21-3011279443-1087069590-2703737120-500 "' % IP_Protocol
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
            print "Successfully installed view broker, pending reboot"
        else:
            print "Installation failed with error code %d" % e.returncode
            raise
    print "NeedsReboot"
    

def autoConfig():
    hostname = ''
    ip= ''
    
    # Now to run the config.bat for broker, it's a special step for broker automation.

def view_broker_installed():
    try:
        output = subprocess.check_output('wmic product get name | find "Connection Server"',shell=True)
        if "Connection Server" in output:
            return True
        else:
            return False
    except:
        return False

def view_broker_HtmlAccess_installed():
    try:
        output = subprocess.check_output('wmic product get name | find "HTML Access"',shell=True)
        if "HTML Access" in output:
            return True
        else:
            return False
    except:
        return False


def get_installed_id(programName):
    output = subprocess.check_output('wmic product get IdentifyingNumber,name |find "%s"' % programName,shell=True)
    if programName in output:
        return output.split(' ')[0]


def uninstall():
    if view_broker_HtmlAccess_installed():
        installed_id = get_installed_id("HTML Access")
        subprocess.call('msiexec /norestart /q/x%s REMOVE=ALL' % installed_id,shell=True)
    if view_broker_installed():
        installed_id = get_installed_id("Connection Server")
        subprocess.call('msiexec /norestart /q/x%s REMOVE=ALL' % installed_id,shell=True)

if __name__ == '__main__':
    install()
    pass
