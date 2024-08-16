from flask import Flask, request
import subprocess
app = Flask(__name__)

@app.route('/stop')
def stop():
    ip = request.args.get('ip')
    cmd = "docker network inspect my_network --format='{{range .Containers}}{{.Name}}:{{.IPv4Address}} {{end}}'"
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    containers = res.stdout.decode().split(" ")
    for container in containers:
        container_name = container.split(":")[0]
        container_ip = container.split(":")[1].split("/")[0]
        if container_ip == ip:
            print(f"Container Name: {container_name}")
            print(f"Container IP: {container_ip}")
            # stop and remove container with subprocess
            cmd = f"docker stop {container_name} && docker rm {container_name}"
            res = subprocess.run(cmd, shell=True)
            if res.returncode == 0:
                print(f"Container with ip: {ip} stopped and removed!")
                return "OK"
            else:
                print("Error:", res.stderr)
                return "OK"
            
    print(f"No container found with IP {ip}")

@app.route('/pkts_info')
def pkts_info():
    pkts = int(request.args.get('pkts'))
    servers = int(request.args.get('servers'))
    print(f"Received {pkts} packets from {servers} servers")

    # open file data.txt and add servers and pkts in that file first column is servers and seconf is pkts

    cmd = f"echo 'GRAPH: {servers},{pkts}'"
    subprocess.run(cmd, shell=True)

    if pkts/servers > 10:
        cmd = f"sudo docker run -d --network=my_network --ip=172.18.0.{str(servers+3)} servernat"
        res = subprocess.run(cmd, shell=True)
        if res.returncode == 0:
            print("Creating new server...")
            return "CREATE_SERVER"
        else:
            print("Error:", res.stderr)
            return "ERROR"
    elif pkts/servers < 5 and servers > 1:
        print("Scaling down...")
        return "STOP_SERVER"
    else:
        return 'OK'

@app.route('/sync')
def sync():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)