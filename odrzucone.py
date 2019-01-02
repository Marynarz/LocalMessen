#Multicast listener as func
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


#data decoder and splitter
def encSliDat(message):
    return message.decode('utf8').split()


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
