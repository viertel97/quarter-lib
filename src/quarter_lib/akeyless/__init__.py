import requests
from dotenv import dotenv_values

env_values = dotenv_values("cred.env")

AUTH_URL = "https://api.akeyless.io/auth"
SECRET_URL = "https://api.akeyless.io/get-secret-value"
TARGET_URL = "https://api.akeyless.io/get-target-details"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json"
}


def __get_token():
    token_response = requests.post(AUTH_URL, json={
        "access-type": "access_key",
        "access-id": env_values['access_id'],
        "access-key": env_values['access_key'],
    }, headers=HEADERS).json()
    return token_response['token']


def get_secrets(secrets: list):
    payload = {
        "accessibility": "regular",
        "names": secrets,
        "pretty-print": True,
        "token": __get_token()
    }
    response = requests.post(SECRET_URL, json=payload, headers=HEADERS).json()
    values = list(response.values())
    if len(values) == 1:
        return values[0]
    return values


def get_target(name: str):
    payload = {
        "show-versions": False,
        "name": name,
        "token": __get_token()
    }
    response = requests.post(TARGET_URL, json=payload, headers=HEADERS).json()
    return response['value']['db_target_details'].values()
