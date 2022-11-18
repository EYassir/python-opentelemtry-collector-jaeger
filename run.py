import requests
import time

while True:
    requests.get("http://localhost:10000/data")
    time.sleep(2)