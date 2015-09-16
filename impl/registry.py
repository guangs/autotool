import _winreg as wreg
import argparse
import threading

class TYPE:
    'Value Type Constants'
    REG_NONE = wreg.REG_NONE
    REG_SZ = wreg.REG_SZ
    REG_EXPAND_SZ = wreg.REG_EXPAND_SZ
    REG_BINARY = wreg.REG_BINARY
    REG_DWORD = wreg.REG_DWORD
    REG_QWORD = 11
    REG_DWORD_BIG_ENDIAN = wreg.REG_DWORD_BIG_ENDIAN
    REG_DWORD_LITTLE_ENDIAN = wreg.REG_DWORD_LITTLE_ENDIAN
    REG_LINK = wreg.REG_LINK
    REG_MULTI_SZ = wreg.REG_MULTI_SZ
    REG_RESOURCE_LIST = wreg.REG_RESOURCE_LIST
    REG_FULL_RESOURCE_DESCRIPTOR = wreg.REG_FULL_RESOURCE_DESCRIPTOR
    REG_RESOURCE_REQUIREMENTS_LIST = wreg.REG_RESOURCE_REQUIREMENTS_LIST

class HKEY:
    'HKEY Constants'
    HKEY_CLASSES_ROOT = wreg.HKEY_CLASSES_ROOT
    HKEY_CURRENT_USER = wreg.HKEY_CURRENT_USER
    HKEY_LOCAL_MACHINE = wreg.HKEY_LOCAL_MACHINE
    HKEY_USERS = wreg.HKEY_USERS
    HKEY_CURRENT_CONFIG = wreg.HKEY_CURRENT_CONFIG

class RIGHT:
    'Access Right Constants'
    QUERY_VALUE = wreg.KEY_QUERY_VALUE
    SET_VALUE = wreg.KEY_SET_VALUE
    CREATE_SUB_KEY = wreg.KEY_CREATE_SUB_KEY
    ENUMERATE_SUB_KEYS = wreg.KEY_ENUMERATE_SUB_KEYS
    NOTIFY = wreg.KEY_NOTIFY
    CREATE_LINK = wreg.KEY_CREATE_LINK
    WRITE = wreg.KEY_WRITE
    EXECUTE = wreg.KEY_EXECUTE
    READ = wreg.KEY_READ
    ALL_ACCESS = wreg.KEY_ALL_ACCESS

class Registry(object):

    lock = threading.Lock()

    def __init__(self):
        object.__init__(self)

    def __split_keypath(self,keypath):
        hkey = keypath.split('\\')[0]
        subkey = '\\'.join(keypath.split('\\')[1:])
        print "hkey is " + hkey
        print "subkey is " + subkey
        return (hkey,subkey)

    def get_value(self,keypath,name):
        '''
        Retrieves the type and data for a specified value name associated with an open registry key.
        The result is a tuple of 2 items if found the key, otherwise, it return None:
        index 0: The value of the registry item
        index 1: An integer giving the registry type for this value, see the mapping ship above
        '''
        try:
            self.lock.acquire()
            hkey, subkey = self.__split_keypath(keypath)
            if hkey in filter(str.isupper, dir(HKEY)):
                key = wreg.OpenKey(HKEY.__dict__.get(hkey),subkey)
                (value, type) = wreg.QueryValueEx(key,name)
                return value
            else:
                return None
        except WindowsError:
            return None
        finally:
            self.lock.release()

    def set_value(self,keypath,name,value,type="REG_SZ"):
        try:
            self.lock.acquire()
            hkey, subkey = self.__split_keypath(keypath)
            if hkey in filter(str.isupper, dir(HKEY)):
                try:
                    key = wreg.OpenKey(HKEY.__dict__.get(hkey), subkey, 0, RIGHT.ALL_ACCESS)
                    #print "update existing reg"
                except WindowsError:
                    key = wreg.CreateKey(HKEY.__dict__.get(hkey), subkey)
                    #print "add new reg"
                if type == 'REG_DWORD':
                    wreg.SetValueEx(key, name, 0, TYPE.__dict__.get(type), int(value))
                elif type == 'REG_SZ':
                    wreg.SetValueEx(key, name, 0, TYPE.__dict__.get(type), value)
                else:
                    'not support'
                    pass
                return True
            else:
                return False
        except WindowsError:
            return False
        finally:
            self.lock.release()

    def del_value(self,keypath,name=None):
        try:
            self.lock.acquire()
            hkey, subkey = self.__split_keypath(keypath)
            if hkey in filter(str.isupper, dir(HKEY)):
                key = wreg.OpenKey(HKEY.__dict__.get(hkey), subkey, 0,RIGHT.ALL_ACCESS)
                if not name:
                    wreg.DeleteKeyEx(HKEY.__dict__.get(hkey),subkey)
                else:
                    wreg.DeleteValue(key,name)
            return True
        except WindowsError:
            return True
        finally:
            self.lock.release()

def print_usage():
    print '''registry model usage:
                      python registry.py get -k <key> -n <name>
                      ptyhon registry.py set -k <key> -n <name> -v <value> -t <type>
                      python registry.py del -k <key> -n <name>
                      '''

def unittest():
    'To test Registry class'
    reg = Registry()
    keypath = r'HKEY_LOCAL_MACHINE\SOFTWARE\Test\temp'
    name = 'buildweb'
    value ='https://buildweb.eng.vmware.com'
    type = 'REG_SZ'
    print reg.set_value(keypath, name, value, type)
    print reg.get_value(keypath, name)
    print reg.del_value(keypath, name)

if __name__ == "__main__":
    'To support command line'
    parser = argparse.ArgumentParser()
    parser.add_argument('func',choices=['get', 'set', 'del'])
    parser.add_argument('-k', '--keypath')
    parser.add_argument('-n', '--name')
    parser.add_argument('-v', '--value')
    parser.add_argument('-t', '--type')
    args = parser.parse_args()
    reg = Registry()
    if args.func == 'get':
        reg.get_value(args.keypath, args.name)
    elif args.func == 'set':
        reg.set_value(args.keypath, args.name, args.value, args.type)
    elif args.func == 'del':
        reg.del_value(args.keypath, args.name)
    else:
        pass


