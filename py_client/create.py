import requests



endpoint = 'http://localhost:8000/api/products/'

data = {
    'title': 'this2',
    'price': 33.9
}

get_response = requests.post(endpoint, json=data)
print(get_response.json())