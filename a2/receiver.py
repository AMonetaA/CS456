from socket import *
import argparse
from packet import Packet

def log_arri(seqnum):
    with open("arrival.log", "a") as file:
        file.write(f"{seqnum}\n")

def clear_files():
    with open("arrival.log","w") as file:
        pass


def main(args):
    r_socket = socket(AF_INET, SOCK_DGRAM)
    r_socket.bind(("", args.rport))
    pbuffer = dict()

    seqnum = 0
    clear_files()

    while True:
        packet, addr = r_socket.recvfrom(2048)
        type, send_seqnum, length, data = Packet(packet).decode()

        
        #send EOT
        if type == 2:
            eot = Packet(2, seqnum, 0, "")
            r_socket.sendto(eot.encode(), (args.host, args.eport))
            log_arri("EOT")
            r_socket.close()
            break
            
        
        # send ack
        if type == 1:
            ack_packet = Packet(0, send_seqnum, 0, "")
            r_socket.sendto(ack_packet.encode(), (args.host, args.eport))
            log_arri(send_seqnum)
            if send_seqnum not in pbuffer:
                pbuffer[send_seqnum] = data

        while seqnum in pbuffer:
            with open(args.file, 'a') as file:
                file.write(pbuffer[seqnum])
                seqnum += 1

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname for the network emulator", type=str)
    parser.add_argument("eport", help="UDP port number used by the link emulator to receive ACKs from the receiver", type=int)
    parser.add_argument("rport", help="UDP port number used by the receiver to receive data from the emulator", type=int)
    parser.add_argument("file", help="name of the file into which the received data is written", type=str)

    args = parser.parse_args()
    main(args)