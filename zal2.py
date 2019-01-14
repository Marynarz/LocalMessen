#import block
import socket
import struct
import threading
import sys

#classes block
class nickBase:
    usersBase = {}
    selfNick = ""

    #constructor
    def __init__(self):
        pass

    #check if key in dict
    def checkNick(self, nick):
        return nick in self.usersBase

    #add key too dict
    def addNick(self, nick, addr):
        self.usersBase[nick] = addr

    def newUser(self):
        succes = False
        while not succes:
            tmpNick = input("Your NICK: ")
            if not self.checkNick(tmpNick):
                sender.setMess("NICK "+ tmpNick)
                if sender.run():
                    self.addNick(tmpNick, '0.0.0.0')
                    self.setSelfNick(tmpNick)
                    succes = True
                else:
                    pass

    def setSelfNick(self,nick):
        self.selfNick = nick

    def getSelfNick(self):
        return self.selfNick


class mCastListen(threading.Thread):
    multicast_group = '224.1.1.1'
    server_address = ('', 10000)
    dataRcv = ''
    addrRcv =''
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
            if not data == sender.mess or self.dataRcv[0] == 'NICK':
                self.addrRcv = address
                self.prnData()
                self.sock.sendto(bytes(self.messValidatin(), 'utf8'), address)



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
                nickB.addNick(temp[1],self.addrRcv)
                result = 'ack'
            else:
                result = 'NICK '+ temp[1] +' BUSY'
        elif temp[0] == 'MSG':
            result = 'ack'
        else:
            result = 'ack'
        return result

class mCastSend(threading.Thread):
    mess =''
    multicast_addr = ('224.1.1.1', 10000)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            ttl = struct.pack('b', 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            sent = sock.sendto(self.mess, self.multicast_addr)

            # Look for responses from all recipients
            while True:
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    break
                else:
                    datatmp = data.decode('utf8').split()
                    if datatmp[0] == 'NICK' and datatmp[2] =='BUSY':
                        return False
                    print(str(server) + ": " +data.decode('utf8'))
        finally:
            #do this silently ;)
            #print('closing socket')
            sock.close()
        return True

    def setMess(self,mess):
        if mess.split()[0] =="NICK":
            self.mess = bytes(mess,'utf8')
        else:
            self.mess = bytes('MSG ' + mess, 'utf8')

#global vars

nickB = nickBase()
sender = mCastSend()
listener = mCastListen()

#func block

#command line tool
def cli():
    listener.start()
    nickB.newUser()

    while True:
        command = input(nickB.selfNick+": ").split()
        if not command:
            pass
        elif command[0].lower() == "exit":
            listener.bye()
            sender.setMess("BYE!")
            sender.run()
            break
        elif command[0].lower() == "listen":
            print("Listener already opened")
            listener.run()
            #listener.join()    do not join, do not bock all program
        elif command[0].lower() == "send":
            sender.setMess(" ".join(command[1::]))
            sender.run()

cli()