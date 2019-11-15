#!/bin/env python
# -*- coding: utf-8 -*-

from calendar_bot.common.global_data import get_value, set_value
from datetime import datetime, timedelta, timezone
from calendar_bot.common.utils import auth_get, auth_post
from calendar_bot.constant import API_BO, OPEN_API
import logging
import pytz
import json

LOGGER = logging.getLogger("calendar_bot")

def get_external_key_from_remote():
    external_key_url = API_BO["TZone"]["external_key_url"]
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    response = auth_post(external_key_url, headers=headers)
    if response.status_code != 200 or response.content is None:
        LOGGER.error("get external key failed. url:%s text:%s body:%s",
                    external_key_url, response.text, response.content)
        raise Exception("get external key. http return code error.")
    tmp_req = json.loads(response.content)
    data = tmp_req.get("data", None)
    if data is None:
        raise Exception("get external key. data filed is None.")
    external_key = data.get("externalKey", None)
    if external_key is None:
        raise Exception("get external key. external_key filed is None.")
    return external_key


def get_external_key():
    external_key = get_value("externalKey", None)
    return external_key


def set_external_key():
    external_key = get_external_key_from_remote()
    set_value("externalKey", external_key)

    return external_key


def load_external_key():
    external_key = get_external_key()
    if external_key is None:
        external_key = set_external_key()
    return external_key
