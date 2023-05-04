from flask import Flask
from flask import request, redirect, make_response
import json
import requests
import random
      
app = Flask(__name__)

baseuri = 'https://dev-16281537.okta.com/oauth2/default/v1/'
state = 'app_state'
clientid = '0oa9dcv4g90yyHGSm5d7'
clientsecret = 'MbedbW_FcD8gsLMXadMYSffnDYdNTpw3YDTBa1Hp'
redirecturi = 'http://localhost:5000/authorization-code/callback'

@app.route('/')
def hello():
    
    authemail=request.cookies.get('email')
    if not authemail:
        url = baseuri + f'authorize?scope=openid email profile&response_type=code&state={state}&client_id={clientid}&redirect_uri={redirecturi}'
        return redirect(url)
    return 'Welcome '+authemail, 200

@app.route('/cookies')
def cookie():
    return request.cookies.get('email')

@app.route('/logout')
def logout():
    authemail=request.cookies.get('email')
    response = make_response('Good bye '+authemail)
    response.delete_cookie('email')
    return response, 200


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

@app.route('/authorization-code/callback')
def callback():
    code=request.args.get("code")
    returnedstate=request.args.get("state")
    if state!=returnedstate:
        return 'wrong state returned', 500
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    authresult = requests.post(baseuri+'token',
                  headers=headers,
                  data=query_params,
                  auth=(clientid, clientsecret)
                  ).json()
    access_token = authresult["access_token"]
    userinfo = requests.get(baseuri+'userinfo',
                            headers={'Authorization': f'Bearer {access_token}'}).json()
    response = make_response(userinfo)
    response.status_code = 200
    response.set_cookie('email', userinfo['email'])
    return response

