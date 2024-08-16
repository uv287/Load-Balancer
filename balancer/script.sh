iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 8000 -j DNAT --to-destination 172.18.0.3:8000
python3 synchronization_client.py
