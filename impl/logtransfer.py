# =====================================================================================
# description     :It is the implementation to transfer collected logs for web service
# author          :Guang Shi
# email           :gshi@vmware.com
# version         :0.1
# date            :2015/9/2
# python version  :2.7
# =====================================================================================
import SocketServer
import logcaptor
import threading
import os
import time

class LogTransferRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        print 'get connection from %s port %s ' % self.client_address
        try:
            data = self.request.recv(1024)
            print data
            if data == 'hello server, I want to get zip log':
                self.request.send('tell me which dir')
                dstdir = self.request.recv(1024)
                dst_dir = logcaptor.LogCaptor._replace_username(dstdir)
                zipfilename = os.path.join(dst_dir,logcaptor.sub_dirname + '.zip')
                if not os.path.exists(zipfilename):
                    self.request.send('zipfile is not existing')
                else:
                    self.request.send('want zipfile name?')
                    if self.request.recv(1024) == 'yes':
                        self.request.send(logcaptor.sub_dirname)
                    if self.request.recv(1024) == 'client ready':
                        self.request.send('server ready')
                    if self.request.recv(1024) == 'go!':
                        print 'starting send file'
                        with open(zipfilename,'rb') as zipfile:
                            while True:
                                data = zipfile.read(4096)
                                if not data:
                                    break
                                self.request.send(data)
                        time.sleep(1)
                        self.request.send('_END_!!!')
                        print 'send file successfully'
                        # remove zip after download
                        os.remove(zipfilename)
            else:
                self.request.send('Not invalid request')
        except Exception, e:
            print e
        # finally:
        #     import time
        #     time.sleep(1)
        #     self.request.close()

    def send_file(self,filename):
        pass




    def login(self):
        'not finished yet'
        self.request.send('please input username')
        username = self.request.recv(1024)
        if username == 'guangs':
            self.request.send('please input password')
        else:
            self.request.send('invalid username')


class LogTransferServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass


server = None
def start_server():
    global server
    HOST = ''
    PORT = 9280
    if server:
        print 'there is server running already'
        return
    server = LogTransferServer((HOST,PORT),LogTransferRequestHandler,bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

def stop_server():
    global server
    if not server:
        print 'server is already closed'
        return
    print 'closing the server'
    server.shutdown()
    server = None

if __name__ == '__main__':
    pass





