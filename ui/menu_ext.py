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
        print 'num or choice: ok (=ok), a (=all), ! (=quit), < (=back), n (=next screen):'

class ViewMenu(Menu):
    raw_input_choices = ['!','<','n']
    @classmethod
    def print_choice(cls):
        print 'num or choice: ! (=quit), < (=back), n (=next screen):'

class MainMenu(ViewMenu):
    items = [('Category','',''),
             ('1.  Configure Logs for Clients and Agents','','menu1'),
             ('2.  Collect Logs from Clients and Agents','','menu2'),
             ('3.  < not support yet >','','menu3'),
             ('4.  < not support yet >','','menu4'),
             ('5.  < not support yet >','','menu5'),
             ('6.  < not support yet >','','menu6'),
             ('7.  < not support yet >','','menu7'),
             ('8.  < not support yet >','','menu8'),
             ('9.  < not support yet >','','menu9'),
             ('10. < not support yet >','','menu10'),
             ('11. < not support yet >','','menu11'),
             ('12. < not support yet >','','menu12'),
             ('13. < not support yet >','','menu13'),
             ('14. < not support yet >','','menu14'),
             ('15. < not support yet >','','menu15'),
             ('16. < not support yet >','','menu16'),
             ('17. < not support yet >','','menu17'),
             ('18. < not support yet >','','menu18'),
             ('19. < not support yet >','','menu19'),
             ('20. < not support yet >','','menu20'),
             ('21. < not support yet >','','menu21'),
             ('22. < not support yet >','','menu22'),]
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


# Menu 1
class LogConfigMenu(EditMenu):
    items = [['Category','Selection',''],
             ['1.  Enable DCT Logs','[ ]','update1'],
             ['2.  Enable ThinPrint Logs','[ ]','update2'],
             ['3.  Enable Serial Logs','[ ]','update3'],
             ['4.  Enable Scanner Logs','[ ]','update4'],
             ['5.  Enable Installer Logs','[ ]','update5'],
             ['6.  Enable PcoIP Logs','[ ]','update6'],
             ['7.  Enable MKS Logs','[ ]','update7'],]
    raw_input_choices = ['ok','a','!','<','n'] + [str(num) for num in range(1,len(items))]
    @classmethod
    def update1(cls):
        if cls.items[1][1] == '[ ]':
            cls.items[1][1] = '[*]'
        else:
            cls.items[1][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update2(cls):
        if cls.items[2][1] == '[ ]':
            cls.items[2][1] = '[*]'
        else:
            cls.items[2][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update3(cls):
        if cls.items[3][1] == '[ ]':
            cls.items[3][1] = '[*]'
        else:
            cls.items[3][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update4(cls):
        if cls.items[4][1] == '[ ]':
            cls.items[4][1] = '[*]'
        else:
            cls.items[4][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update5(cls):
        if cls.items[5][1] == '[ ]':
            cls.items[5][1] = '[*]'
        else:
            cls.items[5][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update6(cls):
        if cls.items[6][1] == '[ ]':
            cls.items[6][1] = '[*]'
        else:
            cls.items[6][1] = '[ ]'
        Frame.exec_menu('LogConfigMenu')
    @classmethod
    def update7(cls):
        if cls.items[7][1] == '[ ]':
            cls.items[7][1] = '[*]'
        else:
            cls.items[7][1] = '[ ]'
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
        else:
            log_flags['DCT'] = False
        if cls.items[2][1] == '[*]':
            log_flags['ThinPrint'] = True
            application.enable_thinprint_logs()
        else:
            log_flags['ThinPrint'] = False
            application.disable_thinprint_logs()
        if cls.items[2][1] == '[*]':
            log_flags['Serial'] = True
        else:
            log_flags['Serial'] = False
        if cls.items[4][1] == '[*]':
            log_flags['Scanner'] = True
        else:
            log_flags['Scanner'] = False
        if cls.items[5][1] == '[*]':
            log_flags['Installer'] = True
        else:
            log_flags['Installer'] = False
        if cls.items[6][1] == '[*]':
            log_flags['PcoIP'] = True
        else:
            log_flags['PcoIP'] = False
        if cls.items[7][1] == '[*]':
            log_flags['MKS'] = True
        else:
            log_flags['MKS'] = False

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


class Frame(object):
    width = 75
    max_items_in_one_page = 10
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
        os.system('cls')
        menu = globals()[menu_class_name]
        cls.total_items = len(menu.items)
        cls.total_pages = cls.total_items/cls.max_items_in_one_page + 1
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
                    func_name = menu.items[int(choice)][2]
                    func = getattr(menu,func_name)
                    func()
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