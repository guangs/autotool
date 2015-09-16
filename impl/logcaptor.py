import os
import re
import shutil
import time
import getpass
import glob
import zipfile
import threading


class LogCaptorException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

sub_dirname = ''
start_time = None
#start_timeout = 60*config_file.StartCaptureLogTimeout
start_timeout = 60*10
common_data = {}
class LogCaptor:
    lock = threading.Lock()
    def __init__(self,src_dir,file_filter=r'.*'):
        self.src_dir = self._replace_username(src_dir)
        if not os.path.exists(self.src_dir):
            raise LogCaptorException('the log src dir is not existing')
        self.file_filter = file_filter
        self.logfiles = [f for f in os.listdir(self.src_dir) if re.match(self.file_filter,f)]
        self.db_key = str.lower(re.sub(r'\\|:|/','_',self.src_dir))

    def start(self):
        global sub_dirname,start_time,common_data
        sub_dirname= time.strftime('%Y%m%d-%H%M')
        start_time = time.time()
        logfiles = self.logfiles
        lastpositions = [self._last_position(os.path.join(self.src_dir,f)) for f in logfiles]
        with self.lock:
            common_data[self.db_key] = []
            common_data[self.db_key] = zip(logfiles,lastpositions)

    def stop(self,dst_dir):
        global sub_dirname,start_time,common_data
        stop_time = time.time()
        if not sub_dirname:
            raise LogCaptorException('please start firstly')
        # if not common_data[self.db_key]:
        #     raise LogCaptorException('common data: please start firstly')
        if stop_time - start_time > start_timeout:
            raise LogCaptorException('timeout, please start again')
        dst_dir = dst_dir + os.sep + sub_dirname
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        # logfiles_before show the files when call start method
        # logfiles_now show the files when call stop method
        # logfile_new show new files during start and stop
        logfiles_before = []
        # handle logfiles_before stop
        for old_file,position in common_data[self.db_key]:
            logfiles_before.append(old_file)
            dst_file = os.path.join(dst_dir,old_file)
            content = ''
            logfile_full_name = os.path.join(self.src_dir,old_file)
            if not os.path.exists(logfile_full_name):
                continue
            with open(logfile_full_name,'r') as tf:
                tf.seek(int(position),0)
                content = tf.read()
            # if no new log, then ignore it, no file created
            if content == '':
                continue
            with open(dst_file,'w') as tf:
                tf.write(content)
        logfiles_now = self.logfiles
        logfile_new = set(logfiles_now) - set(logfiles_before)
        print 'new files: \n', logfile_new
        # handle logfile_new
        for new_file in logfile_new:
            src = os.path.join(self.src_dir,new_file)
            des = os.path.join(dst_dir,new_file)
            shutil.copy(src,des)
        # if no new files in this dir, then remove it
        if not os.listdir(dst_dir):
            os.rmdir(dst_dir)

    @staticmethod
    def _last_position(filename):
        with open(filename,'r') as tf:
            tf.seek(0,2)
            return tf.tell()
    @staticmethod
    def _replace_username(dirname):
        real_username = getpass.getuser()
        return dirname.replace('<username>',real_username)

    @staticmethod
    def zip_logs(dst_dir):
        global sub_dirname
        if not sub_dirname:
            raise LogCaptorException('zip logs: please start firstly')
        if not os.path.exists(dst_dir):
            raise LogCaptorException('please stop firstly and input as same dst_dir as stop method ')
        zipfilename = sub_dirname
        dirname = dst_dir + os.sep + sub_dirname
        if not os.path.exists(dirname):
            raise LogCaptorException('no new logs')
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename + '.zip', 'w', zipfile.ZIP_DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar,arcname)
        zf.close()
        shutil.move(sub_dirname + '.zip',dirname + '.zip')
        # remove folder after zipped
        shutil.rmtree(dirname)

# class LogCaptor2:
#     def __init__(self,src_dir,file_filter=r'.*'):
#         self.src_dir = self._replace_username(src_dir)
#         self.file_filter = file_filter
#         self.logfiles = [f for f in os.listdir(self.src_dir) if re.match(self.file_filter,f)]
#         self.db_file_postfix = str.lower(re.sub(r'\\|:|/','_',self.src_dir))
#         self.db_file = os.getcwd() + os.sep + 'temp' + os.sep + 'db_file_' + self.db_file_postfix + '.txt'
#
#     def start(self):
#         global sub_dirname,start_time
#         sub_dirname= time.strftime('%Y%m%d-%H%M')
#         start_time = time.time()
#         logfiles = self.logfiles
#         print logfiles
#         db_file = self.db_file
#         if not os.path.exists(os.getcwd() + os.sep + 'temp'):
#             os.mkdir(os.getcwd() + os.sep + 'temp')
#         with open(db_file,'w+') as db:
#             for logfile in logfiles:
#                 logfile_full_name = os.path.join(self.src_dir,logfile)
#                 position = self._last_position(logfile_full_name)
#                 sep = ','
#                 line = logfile_full_name + sep + str(position) + '\n'
#                 db.write(line)
#
#     def stop(self,dst_dir):
#         global sub_dirname,start_time
#         stop_time = time.time()
#         if not sub_dirname:
#             raise LogCaptorException('please start firstly')
#         if stop_time - start_time > start_timeout:
#             raise LogCaptorException('timeout, please start again')
#         dst_dir = dst_dir + os.sep + sub_dirname
#         if not os.path.exists(dst_dir):
#             os.mkdir(dst_dir)
#         db_file = self.db_file
#         if not os.path.exists(db_file):
#             pass
#             # raise LogCaptorException('please start firstly')
#         # Parse db_file which was created by start method, store it in db_value
#         db_value = []
#         with open(db_file,'r') as db:
#             line = db.readline()
#             while line:
#                 sep = ','
#                 sep_index = line.index(sep)
#                 db_value.append((line[:sep_index],line[sep_index+1:]))
#                 line = db.readline()
#         if not db_value:
#             raise LogCaptorException('please start firstly')
#         # logfiles_before show the files when call start method
#         # logfiles_now show the files when call stop method
#         # logfile_new show new files during start and stop
#         logfiles_before = []
#         # handle logfiles_before stop
#         for logfile_full_name,position in db_value:
#             old_file = logfile_full_name.split('\\')[-1]
#             logfiles_before.append(old_file)
#             dst_file = os.path.join(dst_dir,old_file)
#             content = ''
#             if not os.path.exists(logfile_full_name):
#                 continue
#             with open(logfile_full_name,'r') as tf:
#                 tf.seek(int(position),0)
#                 content = tf.read()
#             # if no new log, then ignore it, no file created
#             if content == '':
#                 continue
#             with open(dst_file,'w') as tf:
#                 tf.write(content)
#         logfiles_now = self.logfiles
#         logfile_new = set(logfiles_now) - set(logfiles_before)
#         print 'new files: \n', logfile_new
#         # handle logfile_new
#         for new_file in logfile_new:
#             src = os.path.join(self.src_dir,new_file)
#             des = os.path.join(dst_dir,new_file)
#             shutil.copy(src,des)
#         # if no new files in this dir, then remove it
#         if not os.listdir(dst_dir):
#             os.rmdir(dst_dir)
#
#     @staticmethod
#     def _last_position(filename):
#         with open(filename,'r') as tf:
#             tf.seek(0,2)
#             return tf.tell()
#     @staticmethod
#     def _replace_username(dirname):
#         real_username = getpass.getuser()
#         return dirname.replace('<username>',real_username)
#
#     @staticmethod
#     def zip_logs(dst_dir):
#         global sub_dirname
#         if not sub_dirname:
#             raise LogCaptorException('please start firstly')
#         if not os.path.exists(dst_dir):
#             raise LogCaptorException('please stop firstly and input as same dst_dir as stop method ')
#         zipfilename = sub_dirname
#         dirname = dst_dir + os.sep + sub_dirname
#         if not os.path.exists(dirname) or not os.listdir(dirname):
#             raise LogCaptorException('no new logs')
#         filelist = []
#         if os.path.isfile(dirname):
#             filelist.append(dirname)
#         else:
#             for root, dirs, files in os.walk(dirname):
#                 for name in files:
#                     filelist.append(os.path.join(root, name))
#
#         zf = zipfile.ZipFile(zipfilename + '.zip', 'w', zipfile.ZIP_DEFLATED)
#         for tar in filelist:
#             arcname = tar[len(dirname):]
#             #print arcname
#             zf.write(tar,arcname)
#         zf.close()
#         shutil.move(sub_dirname + '.zip',dirname + '.zip')
#         # remove folder after zipped
#         shutil.rmtree(dirname)

if __name__ == '__main__':
    pass
