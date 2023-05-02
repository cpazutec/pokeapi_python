from flask import Flask
from flask import request
import json
import requests
import random
      
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/api1')
def api1s():
    numofreq = int(request.args.get("numofreq"))
    data = ""

    for i in range(numofreq):
        rnd = random.randint(1,1020)
        api_url = "https://pokeapi.co/api/v2/pokemon/"+str(rnd)
        response = requests.get(api_url)
        if response.status_code > 400:
            return "failed "+str(response.status_code), 500
        data += str(response.status_code)
    return data, 200
#http://127.0.0.1:5000/api1
