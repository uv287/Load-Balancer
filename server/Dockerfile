FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-flask \
    python3-requests \
    iptables \
    curl \
    net-tools

COPY server.py /server.py
EXPOSE 8000

COPY synchronization_server.py /synchronization_server.py
EXPOSE 5000

COPY script.sh /script.sh
RUN chmod +x /script.sh

CMD sh -c /script.sh
