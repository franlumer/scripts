#/bin/bash

for start in $(seq 0 5 15); do
    end=$((start+5))
    # discovery de hosts -> nmap-hosts.xml
    echo -sn 192.168.$start-$end.1/24 -oX $REPORT_DIR/nmap-hosts.xml
done