DCTLogEnabled = {'client':['dct_client.reg'],'agent':['dct_agent.reg']}
ThinPrintLogEnabled = {'client':['thinprint_client.reg'],'agent':['thinprint_agent.reg']}

# Define log source dirs
DCTLogDir = {'client':['C:\\Users\\<username>\\AppData\\Local\\VMware\\VDM\\logs',],
             'agent':['C:\\ProgramData\\VMware\\VDM\\logs',]}
ThinPrintLogDir = {'client':['C:\\Temp',],
                   'agent':['C:\\Temp',]}
LogDirs = {'client':
               set(DCTLogDir['client'] + ThinPrintLogDir['client']),
           'agent':
               set(DCTLogDir['agent'] + ThinPrintLogDir['agent'])}

