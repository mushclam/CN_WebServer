import requests, json
from flask import current_app, g

url = 'http://192.168.0.16:5000'

def connection(request):
    target = url + request
    session = requests.Session()
    response = session.get(url=target)

    status = response.status_code
    
    if status == 200:
        return response
    else:
        return Null

def get_json(response):
    body = response.content.decode('utf-8')
    result = json.loads(body)
    return result
