# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calendar_bot.model.data import make_i18n_content_texts, make_button
from calendar_bot.externals.send_message import push_message
from calendar_bot.actions.message import reminder_message, create_button_actions
from calendar_bot.model.processStatusDBHandle import set_status_by_user_date, \
    get_status_by_user

LOGGER = logging.getLogger("calendar_bot")


def sign_out_message():
    actions = create_button_actions("direct_sign_out", "manual_sign_out")
    return make_button("Please select the clock-out time entry method.",
                       actions)


@tornado.gen.coroutine
def sign_out_content(account_id, current_date):

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_out":
            set_status_by_user_date(account_id, current_date, status="in_done")

    if process is None or process != "sign_in_done":
        return reminder_message(None)

    return sign_out_message()


@tornado.gen.coroutine
def sign_out(account_id, current_date, _, __):
    content = yield sign_out_content(account_id, current_date)

    yield push_message(account_id, content)
