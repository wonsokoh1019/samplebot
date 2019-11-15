#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.gen
import asyncio
import time
import uuid
import logging
from datetime import datetime, timedelta
from tornado.web import HTTPError
from calendar_bot.common import global_data
from calendar_bot.common.local_timezone import local_date_time
from calendar_bot.model.data import i18n_text, make_text
from calendar_bot.externals.calendar_req import create_schedule
from calendar_bot.externals.send_message import push_message
from calendar_bot.actions.message import invalid_message, prompt_input
from calendar_bot.model.processStatusDBHandle import get_status_by_user, \
    insert_replace_status_by_user_date
from calendar_bot.model.calendarDBHandle import set_schedule_by_user, \
    get_schedule_by_user

LOGGER = logging.getLogger("calendar_bot")


@tornado.gen.coroutine
def deal_confirm_in(account_id, create_time, callback):
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    user_time = int(str_time)
    my_end_time = user_time + 60
    begin_time = local_date_time(user_time)
    current_date = datetime.strftime(begin_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is not None:
        raise HTTPError(500, "Internal data error")

    end_time = begin_time + timedelta(minutes=1)
    cur_time = local_date_time(create_time)

    schedule_uid = create_schedule(cur_time, end_time, begin_time, account_id)

    set_schedule_by_user(schedule_uid, account_id, current_date,
                         user_time, my_end_time)

    return make_text("Clock-in time has been registered.")


@tornado.gen.coroutine
def confirm_in(account_id, current_date, create_time, callback):
    content = yield deal_confirm_in(account_id, create_time, callback)
    yield push_message(account_id, content)

    insert_replace_status_by_user_date(account_id, current_date,
                                       status="in_done",
                                       process="sign_in_done")
