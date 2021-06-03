import requests

BASE = "http://127.0.0.1:5000/"

response = requests.request(method="GET", url=BASE+'get_all')
print(response.json())