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


def install(product='view',branch='view15h2',buildtype='release',buildid='',kind='official',rds=False,brokerIP='',brokerUsername='hovdi.qa\\administrator',brokerPassword='ca$hc0w'):
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

    if rds:
        msi_v_args = '"/qn VDM_SERVER_NAME=%s VDM_SERVER_USERNAME=%s VDM_SERVER_PASSWORD=%s REBOOT=""ReallySuppress"" "' % (brokerIP,brokerUsername,brokerPassword)
    else:
        msi_v_args = '"/qn REBOOT=""ReallySuppress"" "'
                 
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
        output = subprocess.check_output('wmic product get name | find "VMware Horizon View Agent"',shell=True)
        if "VMware Horizon View Agent" in output:
            return True
        else:
            return False
    except:
        return False

def get_installed_id():
    output = subprocess.check_output('wmic product get IdentifyingNumber,name |find "VMware Horizon View Agent"',shell=True)
    if "VMware Horizon View Agent" in output:
        return output.split(' ')[0]


def uninstall():
    if view_agent_installed():
        installed_id = get_installed_id()
        subprocess.call('msiexec /norestart /q/x%s REMOVE=ALL' % installed_id,shell=True)

if __name__ == '__main__':
    install()
    pass
