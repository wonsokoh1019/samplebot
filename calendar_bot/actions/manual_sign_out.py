#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import asyncio
import logging
from calendar_bot.model.data import i18n_text, make_text
from calendar_bot.externals.send_message import push_messages
from calendar_bot.actions.message import invalid_message, prompt_input
from calendar_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date

LOGGER = logging.getLogger("calendar_bot")


def manual_sign_out_message():
    text1 = make_text("Please manually enter the clock-out time.")

    text2 = prompt_input()

    return [text1, text2]


@tornado.gen.coroutine
def manual_sign_out_content(account_id, current_date):

    yield asyncio.sleep(1)
    content = get_status_by_user(account_id, current_date)

    if content is None or content[1] is None or content[1] != "sign_in_done":
        return [invalid_message()]

    set_status_by_user_date(account_id, current_date, "wait_out")

    return manual_sign_out_message()


@tornado.gen.coroutine
def manual_sign_out(account_id, current_date, _, __):
    contents = yield manual_sign_out_content(account_id, current_date)

    yield push_messages(account_id, contents)
