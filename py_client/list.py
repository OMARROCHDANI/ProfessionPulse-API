import requests

endpoint = 'http://localhost:8000/api/products/'

get_respone= requests.get(endpoint)
print(get_respone.json())


