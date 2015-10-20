""" View client install. """

import requests
import os
import sys
import platform
import urlparse
import subprocess
import tempfile
import buildweb
import threading

INSTALL_PARAMS = [
]


def download_viewclient_installer(product='viewcrt',branch='crt-15q3',buildtype='release',buildid='2999900',kind='official'):
    """ Download the View Client installer from buildweb. """
    # XXX need to make sure ''external_version'' definitively identifies the
    # downloaded MSI.
    arch = 'x86_64' if platform.machine().endswith('64') else 'x86'
    file_pattern = r'VMware-Horizon-View-Client-%s-\d+\.\d+\.\d+\-\d+\.exe' % arch
    return buildweb.download_deliverable_file(
        product,
        file_pattern,
        tempfile.gettempdir(),
        branch,
        buildtype,
        buildid,
        kind)


def install(product='viewcrt',branch='crt-15q3',buildtype='release',buildid='2999900',kind='official'):
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
    
    ## uninstall..
    msi_v_args_uni = '"/qn REMOVE=ALL REBOOT=""ReallySuppress"" "' 
    cmd_and_args_uni = [
        installer_path,
        '/s', # MSI slient install
        '/v', # MSI /v option
        msi_v_args_uni]

    ## install..
    msi_v_args = '"/qn REBOOT=""ReallySuppress"" "'            
    cmd_and_args = [
        installer_path,
        '/s', # MSI slient install
        '/v', # MSI /v option
        msi_v_args]
    
    print 'Starting subprocess:\n    %s' % (' '.join(cmd_and_args))
    try:
        os.system(' '.join(cmd_and_args_uni))
        #subprocess.check_call(' '.join(cmd_and_args), shell=True)
    except subprocess.CalledProcessError as e:
        print "Ignore the uninstall exception."
    
    try:
        subprocess.check_call(' '.join(cmd_and_args), shell=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 3010:
            # install success (3010 means success but needs reboot)
            print "Successfully installed view client, pending reboot"
        else:
            print "Installation failed with error code %d" % e.returncode
            raise
    
    print "NeedsReboot"


def view_client_installed():
    try:
        output = subprocess.check_output('wmic product get name | find "VMware Horizon Client"',shell=True)
        if "VMware Horizon Client" in output:
            return True
        else:
            return False
    except:
        return False

def get_installed_id():
    output = subprocess.check_output('wmic product get IdentifyingNumber,name |find "VMware Horizon Client"',shell=True)
    if "VMware Horizon Client" in output:
        return output.split(' ')[0]

def uninstall():
    if view_client_installed():
        installed_id = get_installed_id()
        subprocess.call('msiexec /norestart /q/x%s REMOVE=ALL' % installed_id,shell=True)

if __name__ == '__main__':
    install()
    pass
