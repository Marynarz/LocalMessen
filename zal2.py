#import block
import socket
import struct
import _thread
from threading import Thread
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

class mCastListen(Thread):
    multicast_group = '224.1.1.1'
    server_address = ('', 10000)
    dataRcv = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def __init__(self):
        Thread.__init__()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            self.encSliDat(data)
            self.prnData()
            sock.sendto(bytes('ack', 'utf8'), address)
        print("Egzit!")
    def encSliDat(self,mess):
        self.dataRcv = mess.decode('utf8').split()
    def prnData(self):
        print(" ".join(self.dataRcv))

#global vars

multicast_addr = ('224.1.1.1',10000)
nickB = nickBase()

#func block

#data decoder and splitter
def encSliDat(message):
    return message.decode('utf8').split()

#Multicast listener
def mCastListener():
    # Multicast Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Multicast Socket options -> re use address
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # Bind to the server address
    sock.bind(server_address)

    # Adding multicast group to all interfaces
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Listener main loop
    while True:
        data, address = sock.recvfrom(1024)
        message = encSliDat(data)
        print(message)
        sock.sendto(bytes('ack','utf8'), address)
    print("Egzit!")

#multicast sender
def mCastSender(mess):
    mess = bytes(mess,'utf8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = sock.sendto(mess, multicast_addr)

        # Look for responses from all recipients
        while True:
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                break
            else:
                datatmp = data.decode('utf8').split()
                print(str(server) + ": " +data.decode('utf8'))

    finally:
        print('closing socket')
        sock.close()
    return True

#command line tool
def cli():
    while True:
        command = input("root: ").split()
        if not command:
            pass
        elif command[0].lower() == "exit":
            _thread.exit()
            break
        elif command[0].lower() == "listen":
            _thread.start_new_thread(mCastListen,())
        elif command[0].lower() == "send":
            s = " ".join(command[1::])
            _thread.start_new_thread(mCastSender,(s,))

cli()