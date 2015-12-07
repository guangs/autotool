# =====================================================================================
# description     :It is the implementation to reboot local windows OS
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/9/2
# python version  :2.7
# =====================================================================================
import subprocess

def reboot():
    subprocess.call('shutdown -r -t 0',shell=True)


def delay_reboot(seconds):
    subprocess.call('shutdown -r -t %d' % seconds,shell=True)


