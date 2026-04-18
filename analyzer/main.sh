#!/bin/bash

# discovery de hosts -> nmap-hosts.xml
nmap -sn 192.168.50.0/24 -oX ../files/nmap-hosts.xml -vvv

# saca todos los hosts con status "up" -> up-hosts.txt
xmlstarlet sel -t -m "//host[status/@state='up']/address" -v "@addr" -n ../files/nmap-hosts.xml > ../files/up-hosts.txt

# escaneo los puertos de los hosts -> ports.xml
sudo nmap -Pn -sSV --top-ports 100 -iL ../files/up-hosts.txt -oX ../files/ports.xml -vvv

python3 xml-analysis.py

# nmap-hosts.xml
# nmaprun
# └── host
#     ├── status (@state="up/down", @reason)
#     ├── address (@addr="45.33.50.110", @addrtype="ipv4")
#     ├── address (@addr="...", @addrtype="mac")  <- solo si está disponible
#     └── hostnames
#         └── hostname (@name, @type)

# nmaprun
# └── host
#     ├── status (@state, @reason)
#     ├── address (@addr, @addrtype)      <- puede haber ipv4 y mac
#     ├── hostnames
#     │   └── hostname (@name, @type)
#     └── ports
#         └── port (@protocol, @portid)
#             ├── state (@state, @reason)
#             └── service (@name, @product, @version, @method)
#                 └── cpe                 <- solo cuando nmap identifica el servicio