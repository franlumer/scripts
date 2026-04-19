import xmltodict

class Host:
    def __init__(self, ip, mac, ports):
        self.ip = ip
        self.mac = mac
        self.ports = ports

def make_list(object):
	if object is None:
		return []
	if not isinstance(object, list):     # verificar si funciona y en caso de que si, cambiarla en el script
		object = [object]
	return object

class_hosts = []

# parsea el xml a dict
with open("../files/ports.xml") as xml:
    xmldict = xmltodict.parse(xml.read())

# accede a nmaprin -> hosts
hosts = xmldict["nmaprun"]["host"]

# en caso de que no sea una lista la convierte en una
# sino no se puede iterar 

hosts = make_list(hosts)

for host in hosts:
	ip = None
	mac = "--"
	ports_list = []

	# solo analiza si el @state es up (host activo)
	if host["status"].get("@state") != "up":
		continue

	addresses = host["address"]
	
	addresses = make_list(addresses)

	for addr in addresses:
		if addr.get("@addrtype") == "ipv4":
			ip = addr.get("@addr")

		elif addr.get("@addrtype") == "mac":
			mac = addr.get("@addr")

	ports = host.get("ports", {})
	port_list = ports.get("port", [])

	port_list = make_list(port_list)

	for port in port_list:
		if port.get("state", {}).get("@state") == "open":
			ports_list.append({
				"port": port.get("@portid"),
				"service": port.get("service", {}).get("@name", "unknown")
			})

	if not ports_list:
		ports_list = "--"
	if ip:
		class_hosts.append(Host(ip, mac, ports_list))

for i in class_hosts:
	print("IP: ", i.ip)
	print("MAC: ", i.mac)
	print("PORTS: ", i.ports)


	