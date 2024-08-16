# Load Balancer / Scaler Project

## Overview

This project focuses on creating a dynamic load balancing system with automatic scaling capabilities for backend servers. The objective is to handle varying loads by adding or removing backend servers dynamically based on demand. This system uses Unix sockets and Docker for deployment and management.

**Course:** CS 695: Topics in Virtualization and Cloud Computing  
**Degree:** Master of Technology in Computer Science and Engineering  
**Authors:** Utsav Manani (23M0788), Aditya Kansara (23M0748)  

## Project Components

1. **Load Balancer**
   - Monitors backend server demand.
   - Notifies the manager to scale up or down backend servers.
   - Adjusts the probability distribution across servers.

2. **Backend Server**
   - Processes client requests.
   - Returns responses via the load balancer.
   - Manages incoming requests for seamless application functionality.

3. **Manager**
   - Orchestrates dynamic scaling of backend servers.
   - Adds or removes backend servers based on demand.


### File Descriptions

- **`run.sh`**: Sets up the load balancing system, including Docker network creation and backend server deployment. Configures IP tables for request distribution and builds the load balancer image.

- **`stop.sh`**: Stops and removes Docker containers and terminates the manager process.

- **`balancer/Dockerfile`**: Sets up the environment for the load balancer with necessary dependencies, including Python 3 and Flask.

- **`balancer/script.sh`**: Configures NAT rules for traffic management and initiates the synchronization client script.

- **`balancer/synchronization_client.py`**: Synchronizes backend servers and relays packet data to the manager.

- **`balancer/hostip.txt`**: Contains the IP address of the host.

- **`balancer/ip.txt`**: Contains IP addresses of currently running backend servers.

- **`manager/script.py`**: Defines a Flask application for managing backend servers, handling routes for stopping containers, receiving packet information, and syncing operations.

- **`server/Dockerfile`**: Sets up the server environment, installs required packages, and specifies the startup script.

- **`server/script.sh`**: Executes the synchronization server and server scripts.

- **`server/synchronization_server.py`**: Initializes a Flask application to handle synchronization requests.

- **`server/server.py`**: Handles client requests on port 8000.

## Tools Used

- **iptables**: For traffic management.
- **Docker**: For containerization and deployment.
- **Flask**: For web server and API management.

