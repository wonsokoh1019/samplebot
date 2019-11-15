#!/bin/env python
# -*- coding: utf-8 -*-

import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import requests
import json
from calendar_bot.constant import API_BO, HEROKU_SERVER_ID, \
    PRIVATE_KEY_PATH, IP_TOKEN


def create_tmp_token(key_path, server_id):
    with open(key_path, "rb") as _file:
        key = _file.read()
        private_key = jwk.JWK.from_pem(key)
        payload = {"iss": server_id}
        token = jwt.generate_jwt(payload, private_key, 'RS256',
                                 datetime.timedelta(minutes=5))
        return token
    return None


def generate_token():
    tmp_token = create_tmp_token(PRIVATE_KEY_PATH, HEROKU_SERVER_ID)
    if tmp_token is None:
        raise Exception("generate tmp token failed.")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8"
    }
    url = API_BO["auth_url"] + tmp_token
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception("generate token failed.")

    content = json.loads(response.content)
    token = content.get("access_token", None)
    if token is None:
        raise Exception("response token is None.")

    return token
