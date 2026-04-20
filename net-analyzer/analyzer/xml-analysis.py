import xmltodict

class Host:
    def __init__(self, ip, mac, ports):
        self.ip = ip
        self.mac = mac
        self.ports = ports

def make_list(object):
	if object is None:
		return []
	if not isinstance(object, list):
		object = [object]
	return object

class_hosts = []

# parsea el xml a dict
with open("../data/ports.xml") as xml:
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

	if ip:
		class_hosts.append(Host(ip, mac, ports_list))

# En este punto la lista class_host ya contiene las instancias de Host.
# El análisis de las mismas debe partir desde ahí.

# 	   	Host
# 	   IP  (str)
#  	  MAC  (str)
# 	PORTS  (list(dict)) 

def report_host(IP: str, PORTS: list):
	if not PORTS:
		pass
		#print(f'''HOST:    {IP}\nPuertos: --\n''')
	else:
		print(f'''HOST:    {IP}\nPuertos: {", ".join(map(str, PORTS))}\n''')


def analyze_host(IP: str, PORTS: list):

	dangerous_ports = [
    '21',    # ftp - sin cifrado
	'22',    # ssh
    '23',    # telnet - sin cifrado
	'80',
    '139',   # netbios - expone recursos de red
	'443',
    '445',   # smb - vector común de ataques
    '111',   # rpcbind - innecesario expuesto
    '2049',  # nfs - no debería estar público
    '3389',  # rdp - expuesto a fuerza bruta
    '6379',  # redis - sin auth por defecto
    '27017', # mongodb - sin auth por defecto
	['80', '443']
	]

	ports_list = []
	open_ports = []

	for port in PORTS:
		port: dict
		ports_list.append(port['port'])

	for dangerous_port in dangerous_ports:
		if isinstance(dangerous_port, list):
			if (set(dangerous_port).issubset(ports_list)):
				open_ports.append(', '.join(map(str, dangerous_port)))

		if dangerous_port in ports_list:
			open_ports.append(dangerous_port)

	report_host(IP, open_ports)

# ==========================================================================================

for host in class_hosts:
	analyze_host(host.ip, host.ports)



	























