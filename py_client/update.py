import requests

endpoint = 'http://localhost:8000/api/products/6/update/'

data = {
'title': 'first data passed by update',
'price': 199,
}

get_respone= requests.put(endpoint, json=data)
print(get_respone.json())


