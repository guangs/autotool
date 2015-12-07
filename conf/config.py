# Lab info
# hostname or IP of all machines
win7x64_client = 'guangs-PC.hovdi.qa'
win10x64_client = 'guangs-win10'

automation_win7 = 'victor-auto-agent.hovdi.qa'
win7x86_agent = 'guangs-win7x86.hovdi.qa'
win7x64_agent = 'guangs-win7x64.hovdi.qa'
win10x64_agent = 'DESKTOP-UV0N5BK.hovdi.qa'
win2012r2_agent = 'guangs-win2012r2.hovdi.qa'
win81x64_agent = 'guangs-win81x64.hovdi.qa'

win2k8_broker = '10.117.46.231'

# My all machines info, install/uninstall/reinstall builds
# suggest configure it using hostname instead of dynamic IP {<host_alias>:<hostname or IP>}
ViewClientHost_All = {'win7x64_client': win7x64_client,
                      'win10x64_client': win10x64_client,
                      'local_client': '127.0.0.1',
                      }
ViewAgentHost_All = {'win7x86_agent': win7x86_agent,
                     'win7x64_agent': win7x64_agent,
                     'automation_win7': automation_win7,
                     'win10x64_agent': win10x64_agent,
                     'win81x64_agent': win81x64_agent,
                     'win2012r2_agent': win2012r2_agent,
                     'local_agent': '127.0.0.1',
                     }
ViewBrokerHost_All = {'win2k8_broker': win2k8_broker,
                      'local_broker': '127.0.0.1',
                      }

# Define which nodes you are using, enable/collect logs on those nodes
ViewClientHost = '127.0.0.1'
ViewAgentHost = win7x64_agent
ViewBrokerHost = '10.117.46.231'


# SaveLogsDirectory = 'C:\\Users\\Administrator\\Desktop\\vdm-sdct-auto'

# 10 min
# StartCaptureLogTimeout = 10




