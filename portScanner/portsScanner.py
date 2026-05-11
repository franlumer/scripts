from scapy.all import IP, TCP, sr1
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='Web scanner')
    parser.add_argument("destIP", help="destination IP")
    return parser.parse_args()

def scann(destIP):
    for port in range(7999, 8001):
        print(f"port: {port}")
        pkt = IP(dst=destIP)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=3, verbose=1)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            print(resp[TCP].flags)
            print(f"Puerto {port} abierto")
        else:
            print(f"Puerto {port} cerrado")



def main():
    args = parseArgs()
    scann(args.destIP)

if __name__ == "__main__":
        main()
