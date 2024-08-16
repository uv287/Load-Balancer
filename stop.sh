#!/bin/bash
var=$(sudo docker ps -aq)
if [ -z "$var" ]; then
    echo "No containers running"
    exit 0
fi
sudo docker stop $var
sudo docker remove $var

sudo kill $(ps -eLf | grep script.py | grep -v grep | awk '{print $2}') 2> /dev/null