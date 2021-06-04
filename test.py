import requests

BASE = "http://127.0.0.1:5000/"

# get current
response = requests.request(method="GET", url=BASE + '/api/PD')
print(len(response.json()))

# get all
response = requests.request(method="GET", url=BASE + '/api/get_all')
print(len(response.json()))

# create ticker bd
response = requests.request(method="POST", url=BASE + '/api/create_db/MSFT', params='MSFT')
print(response)
# upgrade ticker bd
response = requests.request(method="POST", url=BASE + '/api/upgrade/MSFT', params='MSFT')
print(response)
