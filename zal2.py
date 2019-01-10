#import block
import socket
import struct
import threading

#classes block
class nickBase:
    usersBase = {}

    #constructor
    def __init__(self):
        pass

    #check if key in dict
    def checkNick(self, nick):
        return self.usersBase.has_key(nick)

    #add key too dict
    def addNick(self, nick, addr):
        self.usersBase[nick] = addr

class mCastListen(threading.Thread):
    multicast_group = '224.1.1.1'
    server_address = ('', 10000)
    dataRcv = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    thrLoc = ""
    endFlag = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def run(self):
        while True:
            if self.endFlag:
                break
            data, address = self.sock.recvfrom(1024)
            self.encSliDat(data)
            self.prnData()
            self.sock.sendto(bytes('ack', 'utf8'), address)

        print("Bye!")

    def encSliDat(self,mess):
        self.dataRcv = mess.decode('utf8').split()

    def prnData(self):
        print(" ".join(self.dataRcv))

    def bye(self):
        self.endFlag = True

    def messValidatin(self):
        temp = self.dataRcv.split()
        result = 0
        if temp[0] == "NICK":
            if not nickB.checkNick(temp[1]):
                nickB.addNick(temp[1])
                result = 'ack'
            else:
                result = 'NICK '+ temp[1] +' BUSY'
        elif temp[0] == 'MSG':
            pass    #TODO what if message comes here, my friend?
        else:
            result = 'ack'
        return result

class mCastSend(threading.Thread):
    mess =''
    multicast_addr = ('224.1.1.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock.settimeout(1)
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def run(self):
        try:
            sent = self.sock.sendto(self.mess, self.multicast_addr)

            # Look for responses from all recipients
            while True:
                try:
                    data, server = self.sock.recvfrom(16)
                except socket.timeout:
                    break
                else:
                    datatmp = data.decode('utf8').split()
                    print(str(server) + ": " +data.decode('utf8'))
        finally:
            print('closing socket')
            self.sock.close()
        return True
    def setMess(self,mess):
        self.mess = bytes('MSG ' + mess, 'utf8')
#global vars

nickB = nickBase()
sender = mCastSend()
listener = mCastListen()

#func block

#command line tool
def cli():
    while True:
        command = input("root: ").split()
        if not command:
            pass
        elif command[0].lower() == "exit":
            listener.bye()
            listener.join()
            break
        elif command[0].lower() == "listen":
            listener.start()
            #listener.join()    do not join, do not bock all program
        elif command[0].lower() == "send":
            sender.setMess(" ".join(command[1::]))
            sender.run()

cli()