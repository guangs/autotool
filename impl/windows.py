import subprocess

def reboot():
    subprocess.call('shutdown -r -t 0',shell=True)


def delay_reboot(seconds):
    subprocess.call('shutdown -r -t %d' % seconds,shell=True)


