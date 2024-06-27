from django.conf import settings
import json
import requests


def get_auth0_token():
    url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    headers = {'content-type': 'application/json'}
    body = {
        "client_id": settings.AUTH0_CLIENT_ID,
        "client_secret": settings.AUTH0_CLIENT_SECRET,
        "audience": f"{settings.AUTH0_IDENTIFIER}",
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    return response.json()['access_token']


def create_auth0_user(email, password, connection):
    token = get_auth0_token()
    url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users"
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    body = {
        "email": email,
        "password": password,
        "connection": connection
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    return response.json()


def get_auth0_user(user_id):
    token = get_auth0_token()
    url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def update_auth0_user(user_id, data):
    token = get_auth0_token()
    url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()


def delete_auth0_user(user_id):
    token = get_auth0_token()
    url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code == 204
