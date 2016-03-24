# ===============================================================================
# description     :This program displays an interactive menu on CLI for the tool
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/08/30
# python version  :2.7
# ===============================================================================

# Import the modules needed to run the script.
import sys, os
import application
import webclient
import platform
import conf.config as config
import re

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

class Menu(object):
    items = []
    @classmethod
    def on_quit(cls):
        sys.exit()
    @classmethod
    def on_back(cls):
        pass

class EditMenu(Menu):
    raw_input_choices = ['ok','a','!','<','n']
    @classmethod
    def on_all(cls):
        pass
    @classmethod
    def print_choice(cls):
        print 'num or choice: ok (=ok), a (=all), ! (=quit), < (=back), n (=next screen)'

class ViewMenu(Menu):
    raw_input_choices = ['!','<','n']
    @classmethod
    def print_choice(cls):
        print 'num or choice: ! (=quit), < (=back), n (=next screen)'

class MainMenu(ViewMenu):
    items = [('Category','',''),
             ('1.  Configure Logs for test bed','','menu1'),
             ('2.  Collect Logs from test bed','','menu2'),
             ('3.  Enable Blast UDP/TCP for test bed','','menu3'),
             ('4.  Reinstall View Agent Build','','menu4'),
             ('5.  Reinstall View Client Build','','menu5'),
             ('6.  Reinstall View Broker Build','','menu6'),
             ('7.  Get View Agent Build Info','','menu7'),
             ('8.  Get View Client Build Info','','menu8'),
             ('9.  Get View Broker Build Info','','menu9'),
             ('10. Reboot Windows Machines','','menu10'),
             ('11. Activate Local Windows OS','','menu11'),
             ('12. Upgrade AutoTool','','menu12'),
             ('13. <Install .Net Framework>','','menux'),
             ('14. <Install Java>','','menux'),
             ('15. <Install Printers>','','menux'),
             ('16. <Install Microsoft Office>','','menux'),
             ('17. <Install Windows Update>','','menux'),
             ('18. <Create New VM on ESX Host>','','menux'),
             ('19. <Configure Automation>','','menux'),]
    raw_input_choices = ['!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def menu1(cls):
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def menu2(cls):
        Frame.exec_menu('LogCollectMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')
    @classmethod
    def menu3(cls):
        Frame.exec_menu('BlastUDPMenu')
    @classmethod
    def menu4(cls):
        Frame.exec_menu('AgentReinstallMenu')
    @classmethod
    def menu5(cls):
        Frame.exec_menu('ClientReinstallMenu')
    @classmethod
    def menu6(cls):
        Frame.exec_menu('BrokerReinstallMenu')
    @classmethod
    def menu7(cls):
        Frame.exec_menu('AgentBuildInfoMenu')
    @classmethod
    def menu8(cls):
        Frame.exec_menu('ClientBuildInfoMenu')
    @classmethod
    def menu9(cls):
        Frame.exec_menu('BrokerBuildInfoMenu')
    @classmethod
    def menu10(cls):
        Frame.exec_menu('RebootMachineMenu')
    @classmethod
    def menu11(cls):
        import subprocess
        subprocess.call('start C:\\autotool\\scripts\\Microsoft_KMS-MAK_activation.bat',shell=True)
    @classmethod
    def menu12(cls):
        Frame.exec_menu('UpdateAutoToolMenu')
    @classmethod
    def menux(cls):
        print 'Not support yet'


# Menu 1
class LogConfigMenu(EditMenu):
    items = [['Category','Selection',''],
             ['1.  Enable DCT Logs','[ ]','update'],
             ['2.  Enable ThinPrint Logs','[ ]','update'],
             ['3.  Enable Blast Logs','[ ]','update'],
             ['4.  Enable H264 Logs','[ ]','update'],
             ['5.  <Enable Serial Logs>','[ ]','update'],
             ['6.  <Enable Scanner Logs>','[ ]','update'],
             ['7.  <Enable Installer Logs>','[ ]','update'],
             ['8.  <Enable PCoIP Logs>','[ ]','update'],
             ['9.  <Enable MKS Logs>','[ ]','update'],]
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        log_flags = {}
        if cls.items[1][1] == '[*]':
            log_flags['DCT'] = True
            application.enable_dct_logs()
        else:
            log_flags['DCT'] = False
            application.disable_dct_logs()
        if cls.items[2][1] == '[*]':
            log_flags['ThinPrint'] = True
            application.enable_thinprint_logs()
        else:
            log_flags['ThinPrint'] = False
            application.disable_thinprint_logs()
        if cls.items[3][1] == '[*]':
            log_flags['Blast'] = True
            application.enable_blast_logs()
        else:
            log_flags['Blast'] = False
            application.disable_blast_logs()
        if cls.items[4][1] == '[*]':
            log_flags['H264'] = True
            application.enable_h264_logs()
        else:
            log_flags['H264'] = False
            application.disable_h264_logs()
        if cls.items[5][1] == '[*]':
            log_flags['Serial'] = True
            print 'Enable Serial logs successfully'
        else:
            log_flags['Serial'] = False
            print 'Disable Serial logs successfully'
        if cls.items[6][1] == '[*]':
            log_flags['Scanner'] = True
            print 'Enable Scanner logs successfully'
        else:
            log_flags['Scanner'] = False
            print 'Disable Scanner logs successfully'
        if cls.items[7][1] == '[*]':
            log_flags['Installer'] = True
            print 'Enable Installer logs successfully'
        else:
            log_flags['Installer'] = False
            print 'Disable Installer logs successfully'
        if cls.items[8][1] == '[*]':
            log_flags['PCoIP'] = True
            print 'Enable PCoIP logs successfully'
        else:
            log_flags['PCoIP'] = False
            print 'Disable PCoIP logs successfully'
        if cls.items[9][1] == '[*]':
            log_flags['MKS'] = True
            print 'Enable MKS logs successfully'
        else:
            log_flags['MKS'] = False
            print 'Disable MKS logs successfully'

    @classmethod
    def on_quit(cls):
        sys.exit()

# Menu 2
class LogCollectMenu(ViewMenu):
    items =[('Category','',''),
            ("1. Start Capture Logs",'','start'),
            ("2. Stop Capture Logs",'','stop'),]
    raw_input_choices = ['!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def start(cls):
        application.start_capture_logs()

    @classmethod
    def stop(cls):
        application.stop_capture_logs()

    @classmethod
    def on_quit(cls):
        sys.exit()

    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

# Menu 3
class BlastUDPMenu(ViewMenu):
    items =[('Category','',''),
            ("1. Enable Blast UDP",'','enable_udp'),
            ("2. Enable Blast TCP",'','enable_tcp'),
            ]
    raw_input_choices = ['!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def enable_udp(cls):
        application.enable_blast_udp()

    @classmethod
    def enable_tcp(cls):
        application.enable_blast_tcp()

    @classmethod
    def on_quit(cls):
        sys.exit()

    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')


def create_dynamic_menu_items(machines):
    items = [['Machines','Selection',''],]
    sorted_keys = machines.keys()
    sorted_keys.sort()
    for index,key in enumerate(sorted_keys):
        items.append(['%d.  %s' % (index+1, key),'[ ]','update'])
    return items

def create_dynamic_menu_items_without_index(machines):
    items = [['Machines','Selection',''],]
    for machine_alias_name in machines:
        items.append([machine_alias_name,'[ ]','update'])
    return items

# Menu 4
class AgentReinstallMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewAgentHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('AgentReinstallMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('AgentReinstallMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machine = []
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewAgentHost_All[machine_alias_name]
                selected_machine.append(machine_ip)
        if selected_machine:
            application.reinstall_agent(tuple(selected_machine))

    @classmethod
    def on_quit(cls):
        sys.exit()

# Menu 5
class ClientReinstallMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewClientHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('ClientReinstallMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('ClientReinstallMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machine = []
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewClientHost_All[machine_alias_name]
                selected_machine.append(machine_ip)
        if selected_machine:
            application.reinstall_client(tuple(selected_machine))

    @classmethod
    def on_quit(cls):
        sys.exit()


# Menu 6
class BrokerReinstallMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewBrokerHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('BrokerReinstallMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('BrokerReinstallMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machine = []
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewBrokerHost_All[machine_alias_name]
                selected_machine.append(machine_ip)
        if selected_machine:
            application.reinstall_broker(tuple(selected_machine))

    @classmethod
    def on_quit(cls):
        sys.exit()

# Menu 7
class RebootMachineMenu(EditMenu):
    items = []
    items_broker = create_dynamic_menu_items_without_index(config.ViewBrokerHost_All)[1:]
    items_agent = create_dynamic_menu_items_without_index(config.ViewAgentHost_All)[1:]
    items_client = create_dynamic_menu_items_without_index(config.ViewClientHost_All)[1:]
    sorted_items = items_broker + items_agent + items_client
    sorted_items.sort(cmp=lambda x,y: cmp(x[0],y[0]))
    items.append(['Machines','Selection',''])
    for index,item in enumerate(sorted_items):
        if index < 9:
            item[0] = '%d.  ' % (index+1) + item[0]
        else:
            item[0] = '%d. ' % (index+1) + item[0]
        items.append(item)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('RebootMachineMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('RebootMachineMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machine = []
        machine_ip = []
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                if machine_alias_name in config.ViewBrokerHost_All:
                    machine_ip = config.ViewBrokerHost_All[machine_alias_name]
                if machine_alias_name in config.ViewAgentHost_All:
                    machine_ip = config.ViewAgentHost_All[machine_alias_name]
                if machine_alias_name in config.ViewClientHost_All:
                    machine_ip = config.ViewClientHost_All[machine_alias_name]
                selected_machine.append(machine_ip)
        if selected_machine:
            application.reboot_machine(tuple(selected_machine))

    @classmethod
    def on_quit(cls):
        sys.exit()

# Menu 9
class UpdateAutoToolMenu(EditMenu):
    items = []
    items_broker = create_dynamic_menu_items_without_index(config.ViewBrokerHost_All)[1:]
    items_agent = create_dynamic_menu_items_without_index(config.ViewAgentHost_All)[1:]
    items_client = create_dynamic_menu_items_without_index(config.ViewClientHost_All)[1:]
    sorted_items = items_broker + items_agent + items_client
    sorted_items.sort(cmp=lambda x,y: cmp(x[0],y[0]))
    items.append(['Machines','Selection',''])
    for index,item in enumerate(sorted_items):
        if index < 9:
            item[0] = '%d.  ' % (index+1) + item[0]
        else:
            item[0] = '%d. ' % (index+1) + item[0]
        items.append(item)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('UpdateAutoToolMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('UpdateAutoToolMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machine = []
        machine_ip = []
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                if machine_alias_name in config.ViewBrokerHost_All:
                    machine_ip = config.ViewBrokerHost_All[machine_alias_name]
                if machine_alias_name in config.ViewAgentHost_All:
                    machine_ip = config.ViewAgentHost_All[machine_alias_name]
                if machine_alias_name in config.ViewClientHost_All:
                    machine_ip = config.ViewClientHost_All[machine_alias_name]
                selected_machine.append(machine_ip)
        if selected_machine:
            application.update_autotool(tuple(selected_machine))

    @classmethod
    def on_quit(cls):
        sys.exit()


# Menu 10
class AgentBuildInfoMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewAgentHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('AgentBuildInfoMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('AgentBuildInfoMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machines = {}
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewAgentHost_All[machine_alias_name]
                selected_machines[machine_alias_name] = machine_ip
        if selected_machines:
            application.get_agent_buildinfo(selected_machines)

    @classmethod
    def on_quit(cls):
        sys.exit()


# Menu 11
class ClientBuildInfoMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewClientHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('ClientBuildInfoMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('ClientBuildInfoMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machines = {}
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewClientHost_All[machine_alias_name]
                selected_machines[machine_alias_name] = machine_ip
        if selected_machines:
            application.get_client_buildinfo(selected_machines)

    @classmethod
    def on_quit(cls):
        sys.exit()


# Menu 12
class BrokerBuildInfoMenu(EditMenu):
    items = create_dynamic_menu_items(config.ViewBrokerHost_All)
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update(cls,index):
        if cls.items[index][1] == '[ ]':
            cls.items[index][1] = '[*]'
        else:
            cls.items[index][1] = '[ ]'
        Frame.exec_menu('BrokerBuildInfoMenu')
    @classmethod
    def on_all(cls):
        all_true = True
        for Caption,Value,Func in cls.items[1:]:
            if Value == '[ ]':
                all_true = False
        if all_true:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[ ]'
        else:
            for index in range(1,len(cls.items)):
                cls.items[index][1] = '[*]'
        Frame.exec_menu('BrokerBuildInfoMenu')
    @classmethod
    def on_back(cls):
        Frame.exec_menu('MainMenu')

    @classmethod
    def on_ok(cls):
        selected_machines = {}
        for item in cls.items:
            if item[1] == '[*]':
                machine_alias_name = re.findall(r'\d+\.\s\s*(.*)',item[0])[0]
                machine_ip = config.ViewBrokerHost_All[machine_alias_name]
                selected_machines[machine_alias_name] = machine_ip
        if selected_machines:
            application.get_broker_buildinfo(selected_machines)

    @classmethod
    def on_quit(cls):
        sys.exit()


class Frame(object):
    width = 75
    max_items_in_one_page = 12
    curr_menu = None
    curr_menu_choices =None
    total_items = 0
    total_pages = 0
    curr_page = 1
    start_index = 1

    @classmethod
    def center(cls,astring):
        return astring.center(cls.width)

    @classmethod
    def print_title(cls):
        print '-'*cls.width
        print cls.center('Horizon View Windows Client Team Toolkit')
        print '-'*cls.width

    @classmethod
    def print_tail(cls):
        print '-'*cls.width
        cls.curr_menu.print_choice()
        print '-'*cls.width
    @classmethod
    def print_page_num(cls):
        print ('Page %d of %d' % (cls.curr_page,cls.total_pages)).center(cls.width)

    @classmethod
    def print_items(cls):
        if cls.start_index + cls.max_items_in_one_page > cls.total_items:
            end_index = cls.total_items
            for caption,value,action in cls.curr_menu.items[cls.start_index:end_index]:
                if value:
                    print caption + ' '*(cls.width-len(caption)-len(value)) + str(value)
                else:
                    print caption
            for i in range(cls.max_items_in_one_page - (cls.total_items - 1)%cls.max_items_in_one_page):
                print ''
        else:
            end_index = cls.max_items_in_one_page + cls.start_index
            for caption,value,action in cls.curr_menu.items[cls.start_index:end_index]:
                if value:
                    print caption + ' '*(cls.width-len(caption)-len(value)) + str(value)
                else:
                    print caption

    @classmethod
    def print_subtitle(cls):
        blank_len = cls.width - len(cls.curr_menu.items[0][1]) - len(cls.curr_menu.items[0][0])
        print cls.curr_menu.items[0][0] + ' '*blank_len + cls.curr_menu.items[0][1]

    # Execute menu
    @classmethod
    def exec_menu(cls,menu_class_name):
        # clear
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        menu = globals()[menu_class_name]
        cls.total_items = len(menu.items)
        cls.total_pages = (cls.total_items-1)/cls.max_items_in_one_page + (0 if (cls.total_items-1) % cls.max_items_in_one_page == 0 else 1)
        cls.curr_menu = menu
        cls.curr_menu_choices = menu.raw_input_choices
        cls.print_title()
        cls.print_page_num()
        cls.print_subtitle()
        cls.print_items()
        cls.print_tail()
        choice = raw_input("$:")
        while True:
            if choice in cls.curr_menu_choices:
                if choice == 'n':
                    cls.next_screen()
                elif choice == '<':
                    cls.previous_screen()
                elif choice == 'a':
                    cls.on_all()
                elif choice == '!':
                    cls.on_quit()
                elif choice == 'ok':
                    cls.on_ok()
                else:
                    cls.start_index = 1
                    cls.curr_page = 1
                    func_name = menu.items[int(choice)][2]
                    func = getattr(menu,func_name)
                    if isinstance(menu(),ViewMenu):
                        func()
                    else:
                        func(int(choice))
            else:
                cls.exec_menu(cls.curr_menu.__name__)
            choice = raw_input("$:")
    @classmethod
    def on_all(cls):
        cls.curr_menu.on_all()
    @classmethod
    def on_quit(cls):
        sys.exit()
    @classmethod
    def on_ok(cls):
        cls.curr_menu.on_ok()
    @classmethod
    def next_screen(cls):
        if cls.max_items_in_one_page + cls.start_index < cls.total_items:
            cls.start_index += cls.max_items_in_one_page
            cls.curr_page += 1
        cls.exec_menu(cls.curr_menu.__name__)

    @classmethod
    def previous_screen(cls):
        if cls.start_index - cls.max_items_in_one_page > 0:
            cls.start_index -= cls.max_items_in_one_page
            cls.curr_page -= 1
            cls.exec_menu(cls.curr_menu.__name__)
        else:
            cls.curr_menu.on_back()


# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    Frame.exec_menu('MainMenu')