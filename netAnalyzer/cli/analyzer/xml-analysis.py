import xmltodict
import sys

REPORT_DIR = sys.argv[1]
REPORT_LOG = f"{REPORT_DIR}/{sys.argv[2]}.log"

dangerous_ports = []

with open('dangerous-ports.txt', 'r') as dports:
	dports_file = dports.read().splitlines()
	for port in dports_file:
		dangerous_ports.append(port)

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
with open(f"{REPORT_DIR}/nmap-ports.xml") as xml:
    xmldict = xmltodict.parse(xml.read())

# accede a nmaprin -> hosts
hosts = xmldict["nmaprun"].get("host")

# en caso de que no sea una lista la convierte en una
# sino no se puede iterar 

hosts = make_list(hosts)

seen = set()
for host in hosts:
	ip = None
	mac = "--"
	ports_list = []

	# solo analiza si el @state es up (host activo)
#	if host["status"].get("@state") != "up":
#		continue

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
			service = port.get("service", {})
			ports_list.append({
				"port":    port.get("@portid"),
				"service": service.get("@name", "unknown"),
				"product": service.get("@product", ""),
				"version": service.get("@version", ""),
				"status":  port.get("state", {}).get("@state")
			})

	if ip and ip not in seen:
		class_hosts.append(Host(ip, mac, ports_list))

# En este punto la lista class_host ya contiene las instancias de Host.
# El análisis de las mismas debe partir desde ahí.

# 	   	Host
# 	   IP  (str)
#  	  MAC  (str)
# 	PORTS  (list(dict)) 

def report_host(IP: str, PORTS: list):
	
	if PORTS:
		line = f'HOST:    {IP}\nPuertos: {", ".join(map(str, PORTS))}\n'
		print(f'''HOST:    {IP}\nPuertos: {", ".join(map(str, PORTS))}\n''')
		with open(f"{REPORT_LOG}", "a") as log:
			log.write(line)



#def analyze_host(IP: str, PORTS: list):

#	port_service_map = {p['port']: p.get('service', 'unknown') for p in PORTS}
#	ports_list = list(port_service_map.keys())

#	open_ports = []

#	for dangerous_port in dangerous_ports:
#		if isinstance(dangerous_port, list):
#			if set(dangerous_port).issubset(ports_list):
#				entry = ', '.join(
#					f"{p}/{port_service_map.get(p, 'unknown')}"
#					for p in dangerous_port
#				)
#				open_ports.append(entry)

#		elif dangerous_port in ports_list:
#			service = port_service_map.get(dangerous_port, 'unknown')
#			open_ports.append(f"{dangerous_port}/{service}")

#	report_host(IP, open_ports)


def analyze_host(IP: str, PORTS: list):
    open_ports = []
    for p in PORTS:
        port    = p['port']
        service = p.get('service', 'unknown')
        product = p.get('product', '')
        version = p.get('version', '')
        status  = p.get('status', 'unknown')

        # Combina product + version si están disponibles
        ver_str = f" ({product} {version})".strip(" ()") 
        ver_str = f"({ver_str})" if ver_str else ""

        open_ports.append(f"{port}/{service}{ver_str}/{status}")
    report_host(IP, open_ports)


# ==========================================================================================

for host in class_hosts:
	analyze_host(host.ip, host.ports)
