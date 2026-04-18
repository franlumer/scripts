import xmltodict

class Host:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac
        self.ports = []

class_hosts = []

with open("ports.xml") as xml:
    xmldict = xmltodict.parse(xml.read())

hosts = xmldict["nmaprun"]["host"]

for host in hosts:
    ports = host.get("ports", {})
    port_list = ports.get("port", [])

    if not isinstance(port_list, list):
        port_list = [port_list]

    for i in port_list: 
        print(i.get("@portid"), i.get("state").get("@state"))
    #for port in port_list:
        #print(port["@portid"])