# ==================================================================================================
# description     :It is the implementation for cmd line web service, support bat and python
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.2
# date            :2015/11/10
# python version  :2.7
# ==================================================================================================
import registry
import subprocess
import getpass
import os
import re
import registry

class CommandException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_current_user():
    reg = registry.Registry()
    user = reg.get_value('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\LogonUI','LastLoggedOnUser')
    if user:
        return str(user.split('\\')[-1])
    else:
        return 'Administrator'


def client_enable_blast_udp():
    # current_user = getpass.getuser()
    current_user = get_current_user()
    config_ini_dir = 'C:\\Users\\%s\\AppData\\Roaming\\VMware' % current_user
    config_ini_file = os.path.join(config_ini_dir,'config.ini')
    if os.path.exists(config_ini_file) and os.path.isfile(config_ini_file):
        content = ''
        with open(config_ini_file,'r') as f:
            content = f.read()
        udp_pattern = 'RemoteDisplay.enableUDP = [TRUE|FALSE|true|false]*'
        find = re.findall(udp_pattern,content)
        if find:
            new_content = re.sub(udp_pattern,'RemoteDisplay.enableUDP = TRUE',content)
            with open(config_ini_file,'w+') as f:
                f.write(new_content)
        else:
            with open(config_ini_file,'a+') as f:
                f.write('\n')
                f.write('RemoteDisplay.enableUDP = TRUE')
    else:
        with open(config_ini_file,'w') as f:
            f.write('RemoteDisplay.enableUDP = TRUE')


def client_enable_blast_tcp():
    # current_user = getpass.getuser()
    current_user = get_current_user()
    config_ini_dir = 'C:\\Users\\%s\\AppData\\Roaming\\VMware' % current_user
    config_ini_file = os.path.join(config_ini_dir,'config.ini')
    if os.path.exists(config_ini_file) and os.path.isfile(config_ini_file):
        content = ''
        with open(config_ini_file,'r') as f:
            content = f.read()
        udp_pattern = 'RemoteDisplay.enableUDP = [TRUE|FALSE|true|false]*'
        find = re.findall(udp_pattern,content)
        if find:
            new_content = re.sub(udp_pattern,'RemoteDisplay.enableUDP = FALSE',content)
            with open(config_ini_file,'w+') as f:
                f.write(new_content)
        # else:
        #     with open(config_ini_file,'a+') as f:
        #         f.write('\n')
        #         f.write('RemoteDisplay.enableUDP = FALSE')
    # else:
    #     with open(config_ini_file,'w') as f:
    #         f.write('RemoteDisplay.enableUDP = FALSE')


def agent_enable_blast_udp():
    reg = registry.Registry()
    reg.set_value('HKEY_LOCAL_MACHINE\\SOFTWARE\\VMware, Inc.\\VMware Blast\\Config','UdpEnabled','1')
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc stop VMBlast',shell=True)
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc start VMBlast',shell=True)


def agent_enable_blast_tcp():
    reg = registry.Registry()
    reg.del_value('HKEY_LOCAL_MACHINE\\SOFTWARE\\VMware, Inc.\\VMware Blast\\Config','UdpEnabled')
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc stop VMBlast',shell=True)
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc start VMBlast',shell=True)

def broker_enable_blast_udp():
    absg_file = 'C:\\Program Files\\VMware\\VMware View\\Server\\appblastgateway\\absg.properties'
    if os.path.exists(absg_file) and os.path.isfile(absg_file):
        content = ''
        with open(absg_file,'r') as f:
            content = f.read()
        udp_pattern = 'enableUDP=[TRUE|FALSE|true|false]*'
        find = re.findall(udp_pattern,content)
        if find:
            new_content = re.sub(udp_pattern,'enableUDP=true',content)
            with open(absg_file,'w+') as f:
                f.write(new_content)
        else:
            with open(config_ini_file,'a+') as f:
                f.write('\n')
                f.write('enableUDP=true')
    else:
        with open(config_ini_file,'w') as f:
            f.write('enableUDP=true')
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc stop VMBlast',shell=True)
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc start VMBlast',shell=True)


def broker_enable_blast_tcp():
    absg_file = 'C:\\Program Files\\VMware\\VMware View\\Server\\appblastgateway\\absg.properties'
    if os.path.exists(absg_file) and os.path.isfile(absg_file):
        content = ''
        with open(absg_file,'r') as f:
            content = f.read()
        udp_pattern = 'enableUDP=[TRUE|FALSE|true|false]*'
        find = re.findall(udp_pattern,content)
        if find:
            new_content = re.sub(udp_pattern,'enableUDP=false',content)
            with open(absg_file,'w+') as f:
                f.write(new_content)
        else:
            with open(config_ini_file,'a+') as f:
                f.write('\n')
                f.write('enableUDP=false')
    else:
        with open(config_ini_file,'w') as f:
            f.write('enableUDP=false')
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc stop VMBlast',shell=True)
    subprocess.call('ping 127.0.0.1 -n 1',shell=True)
    subprocess.call('sc start VMBlast',shell=True)


client_program_command = {
    'enable_blast_udp': client_enable_blast_udp,
    'enable_blast_tcp': client_enable_blast_tcp,
}

agent_program_command = {
    'enable_blast_udp': agent_enable_blast_udp,
    'enable_blast_tcp': agent_enable_blast_tcp,
}

broker_program_command = {
    'enable_blast_udp': broker_enable_blast_udp,
    'enable_blast_tcp': broker_enable_blast_tcp,
}


def client_execute(command, interpreter):
    # for program type command, it runs
    if interpreter is 'program':
        client_program_command[command]()
    elif interpreter is 'bat':
        bat_execute(command)
    elif interpreter is 'python':
        python_execute(command)
    else:
        raise CommandException('not supported interpreter')


def agent_execute(command, interpreter):
    if interpreter is 'program':
        agent_program_command[command]()
    elif interpreter is 'bat':
        bat_execute(command)
    elif interpreter is 'python':
        python_execute(command)
    else:
        raise CommandException('not supported interpreter')


def broker_execute(command, interpreter):
    if interpreter is 'program':
        broker_program_command[command]()
    elif interpreter is 'bat':
        bat_execute(command)
    elif interpreter is 'python':
        python_execute(command)
    else:
        raise CommandException('not supported interpreter')


# reserved for further
def python_execute(command):
    with open('C:\\Windows\\Temp\\temp.py', 'w+') as temp_file:
        temp_file.write(command)
    subprocess.call('python C:\\Windows\\Temp\\temp.py', shell=True)

# reserved for further
def bat_execute(command):
    with open('C:\\Windows\\Temp\\temp.bat', 'w+') as temp_file:
        temp_file.writelines(command.replace(';','\n'))
        # walk around for update autotool issue: log transfer server could not shutdown when stop Autotool windows service
        if "dispatch.bat" in command:
            import logtransfer,time
            logtransfer.stop_server()
            time.sleep(3)
    try:
        subprocess.check_call('start C:\\Windows\\Temp\\temp.bat', shell=True)
    except subprocess.CalledProcessError as e:
        print "bat execute failed with error code %d" % e.returncode



def program_execute(command):
    print command


def execute(command,interpreter,role=''):
    try:
        # same behavior for client,agent,broker
        if role is '' or role is 'view_client':
            client_execute(command,interpreter)
        elif role is 'view_agent':
            agent_execute(command,interpreter)
        elif role is 'view_broker':
            broker_execute(command,interpreter)
        else:
            raise CommandException('not supported role')
    except Exception,e:
        raise CommandException(e.message())



