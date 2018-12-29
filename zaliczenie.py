import subprocess
import sys
import socket
import struct
import _thread

#var block
procs = []
nick = ''
users = ["admin"]

#subprocess
def subProc():
    procs.append(subprocess.Popen([sys.executable,'zaliczenie.py']))
    for proc in procs:
        proc.wait()

#Multicast listener
def mCastListener():
    print("Listener is alive!")
    #basic config
    multicast_group = '224.1.1.1'
    server_address = ('', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    sock.bind(server_address)
    #adding multicast group to socekt
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('=4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    #main loop of the listener
    while True:
        data, address = sock.recvfrom(1024)
        if data == bytes(str(0xFFF),'utf8'):
            break
        #nick validation
        print(address)
        datatmp = data.decode('utf8').split()

        if datatmp[0] == "NICK":
            if datatmp[0] in users:
                print("Nick already used")
                sock.sendto(bytes("NICK "+datatmp[1]+" BUSY" , 'utf8'), address)
            else:
                users.append(datatmp[1])

        print(data.decode('utf8'))

        sock.sendto(bytes('ack','utf8'), address)

    print("Listener is dead")

def mCastSender(mess):
    print(mess)
    message = bytes(mess,'utf8')
    multicast_group = ('224.1.1.1', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(1)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = sock.sendto(message, multicast_group)

        # Look for responses from all recipients
        while True:
            #print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                break
            else:
                datatmp = data.decode('utf8').split()
                if datatmp[0] == "NICK" and datatmp[2] == "BUSY":
                    return False
                print(str(server) + ": " +data.decode('utf8'))

    finally:
        print('closing socket')
        sock.close()
    return True

def userRegister(userName):
    if userName in users:
        print("Nick already used")
        return False

    mess = "NICK "+userName
    if not mCastSender(mess):
        return False
    return True

#Command line tool
def cli():
    while True:
        name = input("NICK: ")
        result = userRegister(name)
        if result:
            nick = name
            users.append(nick)
            break

    while True:
        command = input(nick + ": ").split()
        if not command:
            pass
        elif command[0].lower() == "exit":
            _thread.exit()
            break
        elif command[0].lower() == "subp":
            subProc()
        elif command[0].lower() == "listener":
            _thread.start_new_thread(mCastListener,())
        elif command[0].lower() == "send":
            s = " "
            s = s.join(command[1::])
            print(s)
            _thread.start_new_thread(mCastSender,(str(nick +": "+s),))
        else:
            print("Wrong command")

cli()