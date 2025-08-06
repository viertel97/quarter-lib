import json
import uuid
from datetime import timedelta

import pandas as pd
import requests

from ..akeyless import get_secrets
from ..logging import setup_logging

logger = setup_logging(__file__)

NOTION_TOKEN = get_secrets("notion/token")

BASE_URL = "https://api.notion.com/v1/"
HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}

def get_databases(databases):
    result_list = []
    for database_id in databases:
        url = BASE_URL + "databases/" + database_id + "/query"
        body = None
        while True:
            r = (
                requests.post(url, headers=HEADERS).json()
                if body is None
                else requests.post(url, data=json.dumps(body), headers=HEADERS).json()
            )
            for results in r["results"]:
                result_list.append(results)
            body = {"start_cursor": r.get("next_cursor")}
            if not r["has_more"]:
                break
    return pd.json_normalize(result_list, sep="~")

def get_database(database_id):
    url = BASE_URL + "databases/" + database_id + "/query"
    result_list = []
    body = None
    while True:
        r = (
            requests.post(url, headers=HEADERS).json()
            if body is None
            else requests.post(url, data=json.dumps(body), headers=HEADERS).json()
        )
        for results in r["results"]:
            result_list.append(results)
        body = {"start_cursor": r.get("next_cursor")}
        if not r["has_more"]:
            break
    return pd.json_normalize(result_list, sep="~")
