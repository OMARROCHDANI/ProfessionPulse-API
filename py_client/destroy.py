import requests

product_id = int(input('give a valid id of the product you want to delete :'))
endpoint = f'http://localhost:8000/api/products/{product_id}/destroy/'
get_respone= requests.delete(endpoint)
print(get_respone.status_code,get_respone.status_code == 204)


