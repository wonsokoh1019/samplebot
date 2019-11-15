#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import json
import pytz
import uuid
import tornado.gen
from tornado.web import HTTPError
from datetime import datetime, timezone
from icalendar import Calendar, Event, Timezone, TimezoneStandard
from calendar_bot.common.utils import auth_get, auth_post, auth_put
from calendar_bot.common.local_timezone import load_time_zone
from calendar_bot.common.local_external_key import load_external_key
from calendar_bot.constant import API_BO, OPEN_API, ADMIN_ACCOUNT, DOMAIN_ID
from calendar_bot.common.global_data import get_value

LOGGER = logging.getLogger("calendar_bot")


def create_headers():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    return headers


def make_icalendar_data(uid, summary, current, end, begin, account_id, create_flag=False):
    cal = Calendar()
    cal.add('PRODID', 'Works sample bot Calendar')
    cal.add('VERSION', '2.0')

    tz = load_time_zone()
    standard = TimezoneStandard()
    standard.add('DTSTART', datetime(1970, 1, 1, 0, 0, 0,
                                     tzinfo=pytz.timezone(tz)))
    standard.add('TZOFFSETFROM', current.utcoffset())
    standard.add('TZOFFSETTO', current.utcoffset())
    standard.add('TZNAME', current.tzname())

    tz = Timezone()
    tz.add_component(standard)
    tz.add('TZID', tz)

    event = Event()
    event.add('UID', uid)

    if create_flag:
        event.add('CREATED', current)

    event.add('DESCRIPTION', account_id)
    event.add('ATTENDEE', account_id)
    event.add('SUMMARY', summary)
    event.add('DTSTART', begin)
    event.add('DTEND', end)
    event.add('LAST-MODIFIED', current)
    event.add('DTSTAMP', current)

    cal.add_component(event)
    cal.add_component(tz)
    schedule_local_string = bytes.decode(cal.to_ical())
    LOGGER.info("schedule:%s", schedule_local_string)
    return schedule_local_string


def create_calendar():

    body = {
        "name": "Attendance management bot",
        "description": "Attendance management bot",
        "invitationUserList": [{
            "email": ADMIN_ACCOUNT,
            "actionType": "insert",
            "roleId": 2
        }]
    }

    headers = create_headers()
    url = API_BO["calendar"]["create_calendar_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    LOGGER.info("create calendar. url:%s body:%s", url, str(body))

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create calendar failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("create calendar id. http response code error.")

    LOGGER.info("create calendar id. url:%s txt:%s body:%s",
                url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create calendar failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise Exception("create calendar id. response no success.")
    return tmp_req["returnValue"]


def create_schedule(current, end, begin, account_id):
    uid = str(uuid.uuid4()) + account_id
    schedule_data = make_icalendar_data(uid, "Clock-in time", current,
                                        end, begin, account_id, True)
    body = {
        "ical": schedule_data
    }

    calendar_id = get_value(API_BO["calendar"]["name"], None)
    if calendar_id is None:
        LOGGER.error("get calendar from cached failed.")
        raise HTTPError(500, "internal error. get calendar is failed.")

    headers = create_headers()
    url = API_BO["calendar"]["create_schedule_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    url = url.replace("_CALENDAR_ID_", calendar_id)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create schedules failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule http code error.")

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")

    LOGGER.info("create schedule. url:%s text:%s body:%s",
                 url, response.text, response.content)

    return_value = tmp_req.get("returnValue", None)
    if return_value is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")

    schedule_uid = return_value.get("icalUid", None)
    if schedule_uid is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")
    return schedule_uid


def modify_schedule(calendar_uid, current, end, begin, account_id):

    calendar_data = make_icalendar_data(calendar_uid, "Working hours",
                                        current, end, begin, account_id)
    body = {
        "ical": calendar_data
    }

    calendar_id = get_value(API_BO["calendar"]["name"], None)
    if calendar_id is None:
        LOGGER.error("get calendar from cached failed.")
        raise HTTPError(500, "internal error. get calendar is failed.")

    url = API_BO["calendar"]["modify_schedule_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    url = url.replace("_CALENDAR_ID_", calendar_id)
    url = url.replace("_CALENDAR_UUID_", calendar_uid)

    headers = create_headers()
    response = auth_put(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("modify schedules failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500,
                        "internal error. create schedule http code error.")

    LOGGER.info("modify schedules. url:%s text:%s body:%s",
                 url, response.text, response.content)

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("modify schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")


def init_calendar():
    calendar_id = create_calendar()
    if calendar_id is None:
        raise Exception("init calendar failed.")
    return calendar_id
