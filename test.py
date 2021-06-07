import requests
from time import time

#test "API"
BASE = "http://127.0.0.1:5000"

# get all
response = requests.request(method="GET", url=BASE + '/api/get_all')
print(response)

# create ticker bd
response = requests.request(method="POST", url=BASE + '/api/create_db/AAAPL', params='AAPL')
print(response)
# upgrade ticker bd
response = requests.request(method="POST", url=BASE + '/api/upgrade/AAPL', params='AAPL')
print(response)

# get current
response = requests.request(method="GET", url=BASE + '/api/AAPL')
print(response)
#Test module2v2

from module1_v2 import frame_to_bd, get_history_data_full
ticker = 'AAPL'
a = time()
get_history_data_full(ticker)
print(time()-a)
a = time()
frame_to_bd(get_history_data_full(ticker), ticker)
print(time()-a)