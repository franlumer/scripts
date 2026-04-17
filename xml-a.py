import xmltodict

class Host:
    def __init__(self, ip, mac, ports):
        self.ip = ip
        self.mac = mac
        self.ports = ports

class_hosts = []

with open("ports.xml") as xml:
    xmldict = xmltodict.parse(xml.read())

hosts = xmldict["nmaprun"]["host"]

if not isinstance(hosts, list):
    hosts = [hosts]

for host in hosts:
	ip = None
	mac = "--"
	ports_list = []

	if host["status"].get("@state") != "up":
		continue

	addresses = host["address"]
	
	if not isinstance(addresses, list):
	    addresses = [addresses]

	for addr in addresses:
		if addr.get("@addrtype") == "ipv4":
			ip = addr.get("@addr")

		elif addr.get("@addrtype") == "mac":
			mac = addr.get("@addr")

	ports = host.get("ports", {})
	port_list = ports.get("port", [])

	if not isinstance(port_list, list):
		port_list = [port_list]

	for port in port_list: 
		if port.get("state", {}).get("@state") == "open":
			ports_list.append({
				"port": port.get("@portid"),
				"service": port.get("service", {}).get("@name", "unknown")
			})
	if ip:
		class_hosts.append(Host(ip, mac, ports_list))

for i in class_hosts:
	print("IP: ", i.ip)
	print("MAC: ", i.mac)
	print("PORTS: ", i.ports)


	