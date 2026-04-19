ports = [
    {'port': '22', 'service': 'ssh'},
    {'port': '80', 'service': 'http'},
    {'port': '443', 'service': 'https'},
    {'port': '21', 'service': 'ftp'},
    {'port': '23', 'service': 'telnet'},
    {'port': '3306', 'service': 'mysql'},
    {'port': '5432', 'service': 'postgresql'},
    {'port': '6379', 'service': 'redis'},
    {'port': '27017', 'service': 'mongodb'},
    {'port': '8080', 'service': 'http-proxy'},
    {'port': '8443', 'service': 'https-alt'},
    {'port': '25', 'service': 'smtp'},
    {'port': '53', 'service': 'dns'},
    {'port': '3389', 'service': 'rdp'},
    {'port': '445', 'service': 'smb'},
    {'port': '139', 'service': 'netbios'},
    {'port': '111', 'service': 'rpcbind'},
    {'port': '2049', 'service': 'nfs'},
]

dangerous_ports = [
    '21',    # ftp - sin cifrado
    '23',    # telnet - sin cifrado
    '139',   # netbios - expone recursos de red
    '445',   # smb - vector común de ataques
    '111',   # rpcbind - innecesario expuesto
    '2049',  # nfs - no debería estar público
    '3389',  # rdp - expuesto a fuerza bruta
    '6379',  # redis - sin auth por defecto
    '27017', # mongodb - sin auth por defecto
	['1', '2']
]

ports_list = []

for port in ports:
	port: dict
	#print(port['port'])

	ports_list.append(port['port'])

for dangerous_port in dangerous_ports:
	if isinstance(dangerous_port, list):
		pass
	if dangerous_port in ports_list:
		print(f"[!] Puerto {dangerous_port} abierto!!")