#!/usr/bin/python3

import sys
from pathlib import Path

try:
    SEARCH = sys.argv[1] 

    servers_file = Path.home() / 'scripts' / 'servers.txt'
    found = False
    
    with open (servers_file, 'r') as SERVERS:  
        lines = SERVERS.readlines()
        for line in lines:
            IP, HOSTNAME = line.strip().split(' - ')
            if SEARCH == IP:
                print(f'[+] {SEARCH} -> {HOSTNAME}')
                found = True

    if not found: 
        print('[!] Server not found')
except Exception as e: 
    print(e)
