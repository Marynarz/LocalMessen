#
# W. Niedzielski 206074
# Marynarz @ github.com
#

#import block
import socket
import struct
import threading

#classes block
#nick base

class NickBase:
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

#room base
class RoomHandler:
    avaliableRooms = []
    activeRoom = ""

    def __init__(self):
        pass

    def checkAval(self):
        sender.setMess("ROOM AVAL")
        sender.run()
        tmp = sender.getAck()
        for r in tmp:
            self.avaliableRooms.append(r)

    def addRoom(self,room):
        if room not in self.avaliableRooms:
            self.avaliableRooms.append(room)

    def roomsAval(self):
        if "ack" in self.avaliableRooms:
            del self.avaliableRooms[self.avaliableRooms.index("ack")]
        return " ".join(self.avaliableRooms)

    def joinRoom(self,roomName):
        sender.setMess("JOIN "+ roomName + " " + nickB.getSelfNick())
        sender.run()
        if roomName not in self.avaliableRooms:
            self.avaliableRooms.append(roomName)
        self.activeRoom = roomName

    def leftRoom(self,bye):
        sender.setMess(" ".join(["LEFT",self.activeRoom,nickB.getSelfNick()]))
        sender.run()
        if not bye:
            self.checkAval()
            print("Rooms: "+ self.roomsAval())
            self.joinRoom(input("Rooms: "))

    def getActiveRoom(self):
        return self.activeRoom

    def whoIs(self):
        sender.setMess("WHOIS "+self.activeRoom)
        sender.run()

#listener
class MCastListen(threading.Thread):
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
            if not data == sender.mess or self.dataRcv[0] in ['NICK','WHOIS']:
                self.addrRcv = address
                self.sock.sendto(bytes(self.messValidatin(), 'utf8'), address)
        print("Bye!")

    def encSliDat(self,mess):
        self.dataRcv = mess.decode('utf8').split()

    def bye(self):
        self.endFlag = True

    def messValidatin(self):
        if self.dataRcv[0] == "NICK":
            if not nickB.checkNick(self.dataRcv[1]):
                nickB.addNick(self.dataRcv[1],self.addrRcv)
                result = 'ack'
            else:
                result = 'NICK '+ self.dataRcv[1] +' BUSY'
        elif self.dataRcv[0] == "ROOM" and self.dataRcv[1] == "AVAL":
            result = rooms.roomsAval()
        elif self.dataRcv[0] == "JOIN" and self.dataRcv[1] == rooms.getActiveRoom():
            print('\x1b[1;31;40m' + self.dataRcv[2]+ " join room!" + '\x1b[0m')
            result = 'ack'
        elif self.dataRcv[0] == "JOIN" and self.dataRcv[1] != rooms.getActiveRoom():
            rooms.addRoom(self.dataRcv[1])
            result = 'ack'
        elif self.dataRcv[0] == "LEFT" and self.dataRcv[1] == rooms.getActiveRoom():
            print('\x1b[1;31;40m' + self.dataRcv[2] + " leave room!" + '\x1b[0m')
            result = 'ack'
        elif self.dataRcv[0] == 'MSG' and self.dataRcv[2] == rooms.getActiveRoom():
            print('\x1b[1;32;40m' + self.dataRcv[1] + ": " + " ".join(self.dataRcv[3::]) + '\x1b[0m')
            result = 'ack'
        elif self.dataRcv[0] =="WHOIS" and self.dataRcv[1] ==rooms.getActiveRoom():
            result = " ".join(["ROOM",rooms.getActiveRoom(),nickB.getSelfNick()])
        else:
            result = 'ack'
        return result

#sender
class MCastSend(threading.Thread):
    mess = ""
    multicast_addr = ('224.1.1.1', 10000)
    ack = []

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.ack.clear()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            ttl = struct.pack('b', 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            sock.sendto(self.mess, self.multicast_addr)

            # Look for responses from all recipients
            while True:
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    break
                else:
                    for a in data.decode('utf8').split():
                        if a not in self.ack:
                            self.ack.append(a)
                    datatmp = data.decode('utf8').split()
                    if datatmp[0] == 'NICK' and datatmp[2] =='BUSY':
                        print('\x1b[1;31;40m' + "Nick busy!" + '\x1b[0m')
                        return False
        finally:
            sock.close()
            if "ROOM" in self.ack:
                del self.ack[self.ack.index("ROOM")]
                del self.ack[self.ack.index(rooms.getActiveRoom())]
                print(" ".join(self.ack))
        return True

    def setMess(self,mess):
        if mess.split()[0] in ["JOIN","NICK","ROOM","LEFT","WHOIS"]:
            self.mess = bytes(mess,'utf8')
        else:
            self.mess = bytes(" ".join(["MSG",nickB.getSelfNick(),rooms.getActiveRoom(),mess]),'utf8') #'MSG ' + nickB.getSelfNick() + " " + rooms.getActiveRoom()+ " " + mess, 'utf8')

    def getAck(self):
        return self.ack

#global vars

nickB = NickBase()
sender = MCastSend()
listener = MCastListen()
rooms = RoomHandler()

#func block
def help():
    print("Chat multicastowy dla sieci lokalnej")
    print("-----------------------------------")
    print("Komendy:")
    print(" : listen - odpalenie nasluchu, !!! Komenda nie dziala !!!")
    print(" : send <wiadomosc> - wysylanie wiadomosci")
    print(" : help - odpalenie tej pomocy")
    print(" : exit - wyjscie z programu")
    print(" : left - wyjscie z pokoju")
    print(" : whois - pokazuje kto jest w aktualnym pokoju")
    print()
    print("Funkcje:")
    print(" : nasluch - nasluch startuje w momencie dpalenia programu i trwa do jego zamkniecia,")
    print("kazda wiadomosc jest decodowana i analizowana pod katem zawartosci")
    print(" : nicki - system oblsuguje system nickow, tak ze kazdy nick jest unikalny w sieci")
    print(" : wysylanie - przed wyslaniem wiadomosci, odpowiedni komunikat jest budowany i enkdowany")
    print("-----------------------------------")

#command line tool
def cli():
    listener.start()
    nickB.newUser()
    rooms.checkAval()
    print("Rooms: "+rooms.roomsAval())
    rooms.joinRoom(input("Room: "))

    while True:
        command = input('\x1b[1;33;41m' + nickB.selfNick + ":" + '\x1b[0m'+" ").split()
        commandMain = command[0].lower()
        if not command:
            pass
        elif commandMain == "exit":
            listener.bye()
            rooms.leftRoom(True)
            sender.setMess("BYE!")
            sender.run()
            listener.join()
            break
        elif commandMain == "listen":
            print("Listener already opened")
            #listener.join()    do not join, do not bock all program
        elif commandMain == "send":
            sender.setMess(" ".join(command[1::]))
            sender.run()
        elif commandMain == "help":
            help()
        elif commandMain == "left":
            rooms.leftRoom(False)
        elif commandMain == "whois":
            rooms.whoIs()
        else:
            print("Wrong command!")

cli()