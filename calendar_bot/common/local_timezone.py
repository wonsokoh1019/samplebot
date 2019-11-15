#!/bin/env python
# -*- coding: utf-8 -*-

import logging
from calendar_bot.common.global_data import get_value, set_value
from datetime import datetime, timedelta, timezone
from calendar_bot.common.utils import auth_get, auth_post
from calendar_bot.common.local_external_key import load_external_key
from calendar_bot.constant import API_BO, DOMAIN_ID, OPEN_API
import pytz
import json

LOGGER = logging.getLogger("calendar_bot")


def get_time_zone():
    external_key = load_external_key()
    time_zone_url = API_BO["TZone"]["time_zone_url"]
    time_zone_url = time_zone_url.replace("DOMAIN_ID", str(DOMAIN_ID))
    time_zone_url = time_zone_url.replace("EXTERNAL_KEY", external_key)

    headers = {
        "content-type": "application/json",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    response = auth_get(time_zone_url, headers=headers)
    if response.status_code != 200 or response.content is None:
        LOGGER.info("get external key failed. url:%s text:%s body:%s",
                    time_zone_url, response.text, response.content)
        raise Exception("get timezone. http code error.")

    tmp_req = json.loads(response.content)
    time_zone = tmp_req.get("timeZone", None)
    if time_zone is None:
        raise Exception("get timezone. no timeZone filed.")
    return time_zone


def get_tz():
    offset_time_zone = get_value("offsetTimeZone", None)
    return offset_time_zone


def set_tz():
    time_zone = get_time_zone()
    set_value("offsetTimeZone", time_zone)

    return time_zone

def load_time_zone():
    time_zone = get_value("offsetTimeZone", None)
    if time_zone is None:
        time_zone = set_tz()

    return time_zone

def local_date_time(time=None):
    tz = load_time_zone()
    if time is not None:
        date_time = datetime.utcfromtimestamp(time)
        utc_dt = date_time.replace(tzinfo=timezone.utc)
        return utc_dt.astimezone(pytz.timezone(tz))

    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(pytz.timezone(tz))

