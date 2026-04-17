#!/bin/bash

nmap -sn portchecker.co -oX nmap-hosts.xml -vvv

# reporte nmap > lista de hosts en txt
xmlstarlet sel -t -m "//host[status/@state='up']/address" -v "@addr" -n nmap-hosts.xml > hosts.txt

sudo nmap -Pn -sSV --top-ports 100 -iL hosts.txt -oX ports.xml -vvv

python3 xml-a.py
