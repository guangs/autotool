#Video Tutorials
1. Demo basic functions [https://youtu.be/3ezQ9-MV0Kk](https://youtu.be/3ezQ9-MV0Kk)  
2. How to configure autotool? Not ready yet  
#Introduction
This tool is designed for VMware View Team. Currently it only supports Windows platform, so it supports view windows broker, windows client and windows agent. However, Mac client and Linux client can also use some functions related to windows VDI, such as "Reinstall View Agent Build" and so forth.   
Here are the basic functions available by now:  
1. Enable/Disable debuglog for test bed  
2. Collect logs from test bed  
3. Enable Blast UDP/TCP for test bed  
4. Reinstall View Agent Build  
5. Reinstall View Client Build  
6. Reinstall View Broker Build  
7. Reboot Windows Machine  
8. Activate Local Windows OS  
9. Upgrade Autotool  (it will fail if your lab could not access to the server sanya.eng.vmware.com)

**Here test bed means the machines you are using to test, in generally, test bed includes one view client, one view agent and one view broker.**
#Installation
######Option 1. If you lab can access to sanya.eng.vmware.com
To install autotool in Machine A, simply access to \\\sanya.eng.vmware.com\Exchange\gshi\automation\autotool from Machine A, then double click "dispatch.bat" to run it, that is all.  

"dispatch.bat" will do the following things automatically for you:  
1. Install python if detect python was not installed in current windows OS.  
2. Copy source code from sanya.eng.vmware.com to local machine (directory c:\autotool).  
3. Install autotool as windows service, and launch it automatically.  

######Option 2. If you lab cann't access to sanya.eng.vmware.com
To install autotool in Machine A. You have to do the following things manually:  
1. Install Python in Machine A  
2. Obtain a copy of autotool   
3. Unzip autotool if needed  
4. Run "manually\_install\_autotool.bat" in the directory of "autotool\bin"  

"manually\_install\_autotool.bat" will install autotool as windows service, and launch it automatically.
######Make sure autotool was installed successfully
Run "services.msc" in command line, and if you can find a windows services called "Autotool" is running, that means autotool was successfully installed.  

**Notice : Please disable firewall or add exception for autotool on port 9180 and 9280**
######Where to get autotool?
The source code is in //depot/documentation/DesktopQE/Beijing/Utility/View/autotool @ perforce-qa.eng.vmware.com:1666

#Configure
Firstly, we need select one machine which installed autotool as "autotool client" to run UI, Actually autotool is all-in-one tool that includes client(to run UI interface) as well as server(to run web service).  

Say that you have installed autotool in Machine A/B/C/D  
Machine A: Running View Client  
Machine B: Running View Agent  
Machine C: Running View Broker  
Machine D: Any windows machine  
Select one machine among them as "autotool client", you can launch UI Menu via double click "autotool\bin\startclient.bat", but before that, you'd better finish autotool configuration.  

######How to configure autotool?   
Go to "autotool\conf" directory, edit config.py file, like this:

    # My all machines info, for install/uninstall/reinstall builds
    # suggest configure it using hostname instead of dynamic IP {<host_alias>:<hostname or IP>}, it is a dict, you 
    # can fill all your machines in it.
    ViewClientHost_All = {'Any alias name for Client Host 1': '<hostname or IP>',
                          'Any alias name for Client Host 2': '<hostname or IP>',}
    ViewAgentHost_All = {'Any alias name for Agent Host 1': '<hostname or IP>',
                         'Any alias name for Agent Host 2': '<hostname or IP>',}
    ViewBrokerHost_All = {'Any alias name for Broker Host 1': '<hostname or IP>',}

    # Define which nodes you are using, for enable/collect logs on those nodes. 
    # Just one machine for ViewClientHost, Just one machine for ViewAgentHost, Just one machine for ViewBrokerHost
    ViewClientHost = 'host name or IP'
    ViewAgentHost = 'host name or IP'
    ViewBrokerHost = 'host name or IP'

**Strongly recommend you configure hostname rather than dynamic IP in config.py**  

#Contribution
If you want to contribute code or get any idea to improve autotool, Please contact Guang Shi   
Email: gshi@vmware.com; Skype: guang.a.shi@gmail.com