import requests, time
import subprocess

def sync_servers():
    backend_servers_ip = []
    running_backend_servers_ip = []
    with open('ip.txt', 'r') as file:
            backend_servers_ip = list(set([line.strip() for line in file.readlines() if line.strip()]))

    for ip in backend_servers_ip:
        try:
            requests.get(f'http://{ip}:5000/sync', timeout=1)
            print(f"Synced with {ip}")
            running_backend_servers_ip.append(ip)
        except requests.RequestException as e:
            print(f"Error syncing with {ip}!")
            stop_server(ip)

    with open('ip.txt', 'w') as file:
        for ip in running_backend_servers_ip:
            file.write(ip + '\n')

def stop_server(ip):
    try:
        hostip = open('hostip.txt', 'r').read().strip()
        res = requests.get(f'http://{hostip}:5000/stop?ip={ip}')
        print(res.text)
    except requests.RequestException as e:
        print("Error stopping server!")

def send_pkt_info_to_manager():
    cmd = "iptables -t nat -L PREROUTING -v -x -Z | tail -n +3 | head -n -1 | awk '{sum+=$1; count+=1} END{print sum, count}'"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        pkt_count = int(res.stdout.split()[0])
        server_count = int(res.stdout.split()[1])
        try:
            hostip = open('hostip.txt', 'r').read().strip()
            res = requests.get(f'http://{hostip}:5000/pkts_info?pkts={pkt_count}&servers={server_count}')
            print(res.text)
            if res.text == "CREATE_SERVER":
                probability = 1/(server_count+1)
                cmd = f"iptables -t nat -I PREROUTING -p tcp --dport 8000 -m statistic --mode random --probability {probability} -j DNAT --to-destination 172.18.0.{server_count+3}:8000 && echo '172.18.0.{server_count+3}' >> ip.txt"
                res = subprocess.run(cmd, shell=True)
                if res.returncode == 0:
                    print("New server with IP: 172.18.0.", server_count+3, "added to load balancer!")
                else:
                    print("Error:", res.stderr)
            elif res.text == "STOP_SERVER":
                cmd1 = "iptables -t nat -L PREROUTING --line-numbers | grep '1.* to:.*' | awk '{print $NF}' | cut -d':' -f2"
                res1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True)          

                cmd2 = "iptables -t nat -D PREROUTING 1"
                res2 = subprocess.run(cmd2, shell=True)
                
                if '\n' in res1.stdout:
                    ip_list = res1.stdout.strip().split('\n')
                else:
                    ip_list = [res1.stdout.strip()]

                remove_ip_from_txt(ip_list[0])
                stop_server(ip_list[0])

                if res1.returncode == 0 and res2.returncode == 0:
                    print("Server stopped!")
                else:
                    print("Error in scalling down!")
                

            else:
                print("No need to create new server!")
        except requests.RequestException as e:
            print("Error sending packet info to manager!")
    else:
        print("Error:", res.stderr)

def get_active_connections():
    cmd = "netstat -tn | grep :8000 | wc -l"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        return int(res.stdout)
    else:
        print("Error:", res.stderr)
        return -1
    
def remove_ip_from_txt(ip):
    with open('ip.txt', 'r') as file:
        ips = [line.strip() for line in file.readlines() if line.strip()]
    with open('ip.txt', 'w') as file:
        for i in ips:
            if i != ip:
                file.write(i + '\n')

while True:
    sync_servers()
    send_pkt_info_to_manager()
    time.sleep(10)
