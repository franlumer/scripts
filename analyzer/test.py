class Host:
	def __init__(self, IP, MAC, PORTS):
		self.IP = IP
		self.MAC = MAC
		self.PORTS = []


hosts = []

for i in range (10):
    hosts.append(Host(f"192.168.50.{i}", "MAC", [1,2,3,4,5,6,7,8,9]))

print(hosts[6].IP)