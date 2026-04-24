#!/bin/bash

DATE=$(date +%Y-%m-%d)
REPORT_DIR=$PWD/../data/"$DATE-report"
mkdir -p $REPORT_DIR

for start in $(seq 150 5 155); 

do
    end=$((start+5))
    # discovery de hosts -> nmap-hosts.xml
    nmap -sn 192.168.$start-$end.1/24 -oX $REPORT_DIR/nmap-hosts.xml  

    # saca todos los hosts con status "up" -> up-hosts.txt
    xmlstarlet sel -t -m "//host[status/@state='up']/address" -v "@addr" -n $REPORT_DIR/nmap-hosts.xml > $REPORT_DIR/up-hosts.txt

    # escaneo los puertos de los hosts -> ports.xml
    sudo nmap -Pn -sSV --top-ports 100 -iL $REPORT_DIR/up-hosts.txt -oX $REPORT_DIR/nmap-ports.xml

    python3 xml-analysis.py $REPORT_DIR
done

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
