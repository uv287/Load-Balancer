FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-flask \
    python3-requests \
    iptables \
    curl \
    net-tools

COPY synchronization_client.py /synchronization_client.py
COPY ip.txt /ip.txt
COPY script.sh /script.sh
COPY hostip.txt /hostip.txt

RUN chmod +x /script.sh

CMD sh -c /script.sh