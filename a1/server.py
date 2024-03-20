from socket import *
import sys, os

storage_dir = ""
command = ""
r_port = 0

def is_file_exist(filename):
    files = os.listdir(storage_dir)
    return filename in files



def handle_get(client_addr, filename, port):
    # Stage 1
    # Negotiation using UDP sockets
    # Find if the file exist
    print("Handling GET")
    if is_file_exist(filename):
        r_port = port
        msg = "200 OK"
        s_udp.sendto(msg.encode(), client_addr)
    else: 
        msg = "404 Not Found"
        s_udp.sendto(msg.encode(), client_addr)
        print("404 Not Found")
        return

    # Stage 2
    # Transaction using TCP sockets
    # create TCP socket and connect to client
    s_tcp = socket(AF_INET, SOCK_STREAM)
    s_tcp.connect((client_addr[0], r_port))

    # read file
    path = os.path.join(storage_dir, filename)
    with open(path, 'rb') as file:
        data = file.read(1024)
        while(data):
            s_tcp.send(data)
            data = file.read(1024)
        print("User successfully downloaded")   
    


def handle_put(client_addr, filename):
    s_tcp = socket(AF_INET, SOCK_STREAM)
    s_tcp.bind(('', 0))
    s_tcp.listen()

    print("Handling PUT")
    # Stage 1
    # Negotiation using UDP socket
    r_port = s_tcp.getsockname()[1]
    s_tcp.listen()
    msg = str(r_port)
    s_udp.sendto(msg.encode(), client_addr)

    # Stage 2
    # Recving file using TCP socket
    conn, addr = s_tcp.accept()
    path = os.path.join(storage_dir, filename)
    with open(path, 'wb') as file:
        while 1:
            temp = conn.recv(1024)
            if not temp:
                break
            file.write(temp)
        print("User successfully uploaded")


def handleRequest(s_udp, n_port):
    # revieve command, filename (and port) from client
    msg, client_addr = s_udp.recvfrom(1024)
    print(f"Connection from {client_addr}")
    recv_data = msg.decode()

    # find if command is GET of PUT
    result = recv_data.split(',')
    command = result[0]
    if command == "GET" :
        filename = result[1]
        port = result[2]
        handle_get(client_addr, filename, int(port))

    else:
        filename = result[1]
        handle_put(client_addr, filename)


if __name__ == '__main__':
    storage_dir = sys.argv[1]

    # Create a udp socket
    s_udp = socket(AF_INET, SOCK_DGRAM)
    s_udp.bind(('', 0))
    n_port = s_udp.getsockname()[1]

    # printing port number
    print("Server n_port: " + str(n_port))
    print("Waiting for connection...")
    while 1:
        handleRequest(s_udp, n_port)

 
    

        