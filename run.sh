#!/bin/bash
> ./balancer/ip.txt
> ./balancer/script.sh
> ./balancer/hostip.txt

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# if my_network subnet is not created
if [ -z $(sudo docker network ls --filter name=my_network --format="{{.Name}}") ]; then
    echo "Creating network..."
    $(sudo docker network create --subnet=172.18.0.0/16 my_network)
fi

# how many containers to run
echo "How many servers do you want to run?"
read num

if [ $num -lt 1 ]; then
    echo "Number of servers must be greater than 0"
    exit
fi

for i in $(seq 3 $((num+2))); do
    echo -n "Running server $(($i-2))... "
    echo "172.18.0.$i" >> ./balancer/ip.txt
    sudo docker run -d --network=my_network --ip=172.18.0.$i servernat
done

# create rules for balancer add it to ./balancer/script.sh
echo "Creating rules for balancer..."
echo "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE" >> ./balancer/script.sh
for i in $(seq 4 $((num+2))); do
    probability=$(echo "scale=7; 1/($num+4-$i)" | bc)
    ip=$(echo "$num+2+4-$i" | bc)
    echo "iptables -t nat -A PREROUTING -p tcp --dport 8000 -m statistic --mode random --probability $probability -j DNAT --to-destination 172.18.0.$ip:8000" >> ./balancer/script.sh
done
echo "iptables -t nat -A PREROUTING -p tcp --dport 8000 -j DNAT --to-destination 172.18.0.3:8000" >> ./balancer/script.sh
echo "python3 synchronization_client.py" >> ./balancer/script.sh

hostname -I | awk '{print $1}' > ./balancer/hostip.txt
echo "Building balancer image..."
$(sudo docker build -t balancernat ./balancer)


sudo python3 ./manager/script.py 2>&1 /dev/null &
# sudo python3 ./manager/script.py

echo -n "Running balancer..."
sudo docker run -it --cap-add=NET_ADMIN --network=my_network --ip=172.18.0.2 balancernat
