#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.gen
import asyncio
import time
import logging
from datetime import datetime
from tornado.web import HTTPError
from calendar_bot.common import global_data
from calendar_bot.common.local_timezone import local_date_time
from calendar_bot.model.data import i18n_text, make_text
from calendar_bot.externals.calendar_req import modify_schedule
from calendar_bot.externals.send_message import push_messages
from calendar_bot.actions.message import invalid_message, prompt_input, \
    TimeStruct, number_message
from calendar_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date
from calendar_bot.model.calendarDBHandle import get_schedule_by_user, \
    modify_schedule_by_user

LOGGER = logging.getLogger("calendar_bot")


def confirm_out_message(user_time, hours, min):
    user_time = TimeStruct(user_time)

    return make_text("Clock-out time has been registered."
                     "The total working hours for {date} "
                     "is {hours} hours and {minutes} minutes."
                     .format(date=user_time.date_time.strftime('%A, %B %d'),
                             hours=hours, minutes=min))


@tornado.gen.coroutine
def deal_confirm_out(account_id, create_time, callback):
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    user_time = int(str_time)

    end_time = local_date_time(user_time)
    current_date = datetime.strftime(end_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is None:
        raise HTTPError(500, "Internal data error")
    schedule_id = info[0]
    begin_time_st = info[1]

    cur_time = local_date_time(create_time)
    begin_time = local_date_time(begin_time_st)
    modify_schedule(schedule_id, cur_time, end_time, begin_time, account_id)

    modify_schedule_by_user(schedule_id, user_time)

    if user_time < begin_time_st:
        yield asyncio.sleep(1)
        set_status_by_user_date(account_id, current_date, status="wait_out")
        return number_message(), False

    hours = int((user_time - begin_time_st)/3600)
    min = int(((user_time - begin_time_st) % 3600)/60)

    return [confirm_out_message(user_time, hours, min)], True


@tornado.gen.coroutine
def confirm_out(account_id, current_date, create_time, callback):

    contents, success = yield deal_confirm_out(account_id, create_time, callback)

    yield push_messages(account_id, contents)

    if success:
        set_status_by_user_date(account_id, current_date,
                                status="out_done", process="sign_out_done")
