from socket import *
import sys, os, struct

server_addr = ""
n_port = ""
command = ""
filename = ""
chunksize = int(1024)
r_port = 0



def get (s_udp, filename):
    # create TCP socket to connect server later
    s_tcp = socket(AF_INET, SOCK_STREAM)
    s_tcp.bind(('', 0))
    r_port = s_tcp.getsockname()[1]
    s_tcp.listen()

    # Stage 1
    # Negotiation using UDP sockets
    msg = f"{command},{filename},{r_port}"
    s_udp.send(msg.encode())
    result = s_udp.recv(1024).decode()
    print(result)

    # if file doew not exist, return
    if result == "404 Not Found":
        s_tcp.close()
        return
    print("Find file. Ready for TCP connection")
    
    # Stage 2
    # Transaction using TCP sockets
    conn, addr = s_tcp.accept()
    with open(filename, 'wb') as file:
        while 1:
            temp = conn.recv(1024)
            if not temp:
                break
            file.write(temp)
        print("Successfully downloaded") 



def put (s, filename):
    # Stage 1
    # Negotiation using UDP socket
    msg = f"{command},{filename}"
    s_udp.send(msg.encode())
    r_port = s_udp.recv(1024).decode()
    print("Connected to server, TCP port number " + r_port)

    # Stage 2
    # Sending file using TCP socket
    s_tcp = socket(AF_INET, SOCK_STREAM)
    s_tcp.connect((server_addr, int(r_port)))
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while(data):
            s_tcp.send(data)
            data = file.read(1024)
        print("Successfully uploaded")  



if __name__ == '__main__':
    server_addr = sys.argv[1]
    n_port = sys.argv[2]
    command = sys.argv[3]
    filename = sys.argv[4]
    n_port = int(n_port)

    # create UDP socket and connect to server
    s_udp = socket(AF_INET, SOCK_DGRAM)
    s_udp.connect((server_addr, n_port))
    print("Connect to " + server_addr + ", UDP port " + str(n_port))
    
    
    if command == "GET":
        get(s_udp, filename)
    elif command == "PUT":
        put(s_udp, filename)
    else: print("invalid command")

