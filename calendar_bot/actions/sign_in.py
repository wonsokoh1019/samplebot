# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calendar_bot.model.data import make_i18n_content_texts, make_button
from calendar_bot.externals.send_message import push_message
from calendar_bot.actions.message import reminder_message, create_button_actions
from calendar_bot.model.processStatusDBHandle import delete_status_by_user_date, \
    get_status_by_user

LOGGER = logging.getLogger("calendar_bot")


def sign_in_message():
    actions = create_button_actions("direct_sign_in", "manual_sign_in")

    return make_button("Register current time as clock-in time",
                       actions)


@tornado.gen.coroutine
def sign_in_content(account_id, current_date):

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_in":
            delete_status_by_user_date(account_id, current_date)

    if process is not None:
        return reminder_message("sign_in_done")

    return sign_in_message()


@tornado.gen.coroutine
def sign_in(account_id, current_date, _, __):
    content = yield sign_in_content(account_id, current_date)

    yield push_message(account_id, content)
