import sys

try:
    SEARCH = sys.argv[1] 

    with open ('servers.txt', 'r') as SERVERS:  
        lines = SERVERS.readlines()
        for line in lines:
            IP, HOSTNAME = line.split(' - ')
            if SEARCH == IP:
                print(f'{SEARCH} -> HOSTNAME')
except Exception as e: 
    print(e)
