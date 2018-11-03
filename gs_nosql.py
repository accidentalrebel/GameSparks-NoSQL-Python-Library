#!/usr/bin/env python3
import os
import requests
import json

AUTH_URL = 'https://auth.gamesparks.net/restv2/auth'
GAME_URL = 'https://config2.gamesparks.net/restv2/game/'

access_token = None
stage_base_url = None
jwt_token = None
api_key = None

def authenticate(is_live = False):
    global access_token
    global stage_base_url
    global jwt_token
    global api_key

    if stage_base_url:
        print('Already logged in.')
        return

    auth_file = open(os.path.expanduser('~') + '/.gs-auth', 'r')
    auth_data = json.load(auth_file)
    auth_file.close()

    user_name = auth_data['user_name']
    password = auth_data['password']
    api_key = auth_data['api_key']

    access_token = get_access_token(user_name, password)
    print('Access token retrieved.')

    stage_base_url = get_endpoint(access_token, api_key, is_live)
    if is_live:
        print('Stage Base URL for LIVE retrieved.')
    else:
        print('Stage Base URL for PREVIEW retrieved.')

    jwt_token = get_jwt_token(access_token, api_key)
    print('JWT Token retrieved.\n')

def get_access_token(username, password):
    url = AUTH_URL + '/user'
    res = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
    if res.status_code != 200:
        print('Invalid Credentials')
    return res.json()['X-GSAccessToken']

def get_jwt_token(token, api_key):
    url = AUTH_URL + '/game/' + api_key + '/jwt'
    res = requests.get(url, params={ 'X-GSAccessToken': token })
    if res.status_code != 200:
        print('Failed to get JWT Token with ' + str(res.status_code) + ' status code.')
    return res.json()['X-GS-JWT']

def get_endpoint(token, api_key, is_live):
    url = GAME_URL + api_key + '/endpoints'
    res = requests.get(url, params={ 'X-GSAccessToken': token })
    if res.status_code != 200:
        print('Failed to get end points with ' + str(res.status_code) + ' status code.')

    if is_live:
        return res.json()['liveNosql']

    return res.json()['previewNosql']

def collection_find(collection, data):
    assert isinstance(data, str)
    assert stage_base_url

    url = stage_base_url + '/restv2/game/' + api_key + '/mongo/collection/' + collection + '/find'
    headers = {
        'X-GS-JWT': jwt_token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json'
    }
    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 200:
        print('Failed to find in collection with ' + str(res.status_code) + ' status code.')
    return res.json()

def collection_update(collection, data):
    assert isinstance(data, str)
    assert stage_base_url

    url = stage_base_url + '/restv2/game/' + api_key + '/mongo/collection/' + collection + '/update'
    headers = {
        'X-GS-JWT': jwt_token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json'
    }
    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 200:
        print('Failed to update the collection with ' + str(res.status_code) + ' status code.')
    else:
        print('Successfully updated the collection')
