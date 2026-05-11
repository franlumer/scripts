from scapy.all import IP, TCP, sr1

for port in range(60, 81):
    pkt = IP(dst="https://scanme.nmap.org/")/TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=1)
    if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
        print(f"Puerto {port} abierto")
    elif resp and resp.haslayer(TCP) and resp[TCP].flags == None:
        print(f"Puerto {port} cerrado")