import requests
import threading
import time

def send_request(url):
    while True:
        requests.get(url)
        time.sleep(1)  # Send request every 0.1 seconds

if __name__ == "__main__":
    url = "http://172.18.0.2:8000"
    
    # Create multiple threads to send requests asynchronously
    num_threads = 30
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request, args=(url,))
        threads.append(thread)
        thread.start()
