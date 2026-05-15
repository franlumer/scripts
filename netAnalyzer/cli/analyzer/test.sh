#/bin/bash

while getopts ":vo:ao:" opt; do
    case "$opt" in
        v) 
        echo "-v"
        ;;
        a) 
        echo "-a"
        ;;
    esac 
done

