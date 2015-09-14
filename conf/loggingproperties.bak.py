ThinPrintLogEnabled = {'client':['buildweb.reg'],'agent':['enabledthinprint.reg']}
ThinPrintLogDir = {'client':['C:\\Users\\<username>\\Desktop\\srcdir',
                             'C:\\Users\\<username>\\AppData\\Local\\VMware\\VDM\\logs'],
                   'agent':['C:\\Users\\<username>\\Desktop\\srcdir',
                            'C:\\ProgramData\\VMware\\VDM\\logs']}


LogDirs = {'client':
               set(ThinPrintLogDir['client']),
           'agent':
               set(ThinPrintLogDir['agent'])}

