from socket import *
from packet import Packet
import time
import argparse
from datetime import datetime

def log_seqnum(seqnum):
    with open("seqnum.log", "a") as file:
        file.write(f"{seqnum}\n")

def log_ack(ack):
    with open("ack.log", "a") as file:
        file.write(f"{ack}\n")

def clear_files():
    with open("seqnum.log","w") as file:
        pass
    with open("ack.log","w") as file:
        pass

def main(args):
    max_len = 500
    seqnum = 0
    max_packet = 10


    s_socket = socket(AF_INET, SOCK_DGRAM)
    s_socket.bind(("", args.rport))

    sender_window = dict()
    packetsdata = []
    seqnum = 0
    clear_files()
    # store the file as packets in a list
    with open(args.file, 'r') as file:
        while True:
            data = file.read(max_len)
            if not data:
                break
            # packetsdata.append(Packet(1, seqnum, len(data), data))
            packetsdata.append(data)
            seqnum += 1

    # for d in packetsdata:
    #     print(d)
    seqnum = 0
    while True:

        
        # send the currernt pkt and store it into the sender window
        # does not exceed # of max packet
        while len(sender_window.keys()) < max_packet and seqnum < len(packetsdata):
            packet = Packet(1, seqnum, len(packetsdata[seqnum]), packetsdata[seqnum])
            s_socket.sendto(packet.encode(), (args.host, args.eport))
            log_seqnum(seqnum)
            sender_window[seqnum] = packet
            # record currerent packet that is sent
            seqnum += 1
        
        

        currtime = datetime.now()

        # # recive acks when there are still pkts in the sender window
        # print(len(sender_window.keys()))
        if len(sender_window.keys()) > 0:
            while True:
                if (datetime.now() - currtime).microseconds >= args.timeout: 
                    break

                packet, _ = s_socket.recvfrom(2048)
                type, ack_seqnum, length, data = Packet(packet).decode()
                # pop the pkt if it is acked
                print(ack_seqnum)
                if ack_seqnum in sender_window:
                    sender_window.pop(ack_seqnum, 0)
                    log_ack(ack_seqnum)
        # send the pkt again when timeout
        
            for rseqnum, rpacket in sender_window.items():
                print("resend")
                s_socket.sendto(rpacket.encode(), (args.host, args.eport))
                log_seqnum(rseqnum)

        # when no pkt in sender window and seqnum reach the end of the packet list 
        # send EOT
        if len(sender_window.keys()) == 0 and seqnum >= len(packetsdata): 
            eot = Packet(2, seqnum, 0, "")
            s_socket.sendto(eot.encode(), (args.host, args.eport))
            break
    
    # wait on eot from the reviever and quit
    while True:
        packet, _ = s_socket.recvfrom(2048)
        type, ack_seqnum, length, data = Packet(packet).decode()
        if type == 2:
            log_ack("EOT")
            log_seqnum("EOT")
            s_socket.close()
            break




if __name__ == "__main__":
    ## parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("host", help="host address of the network emulator", type=str)
    parser.add_argument("eport", help="UDP port number used by the emulator to receive data from the sender", type=int)
    parser.add_argument("rport", help="port number used by the sender to receive ACKs from the emulator", type=int)
    parser.add_argument("timeout", help="timeout interval in units of millisecond", type=int)
    parser.add_argument("file", help="name of the file to be transferred", type=str)

    args = parser.parse_args()
    main(args)