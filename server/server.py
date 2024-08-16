from flask import Flask, request
import socket
app = Flask(__name__)

@app.route('/')
def serve():
    ip = socket.gethostbyname(socket.gethostname())
    limit = 1000
    primes = [i for i in range(2, limit) if is_prime(i)]
    return f'Computed", {len(primes)}, "prime numbers up to", {limit} by Server: {ip}\n'

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)