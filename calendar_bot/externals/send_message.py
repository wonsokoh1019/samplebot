#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import json
import tornado.gen
from tornado.web import HTTPError
from calendar_bot.common.utils import auth_post, replace_url_bot_no
from tornado.httpclient import AsyncHTTPClient
from calendar_bot.constant import API_BO, OPEN_API

LOGGER = logging.getLogger("calendar_bot")


@tornado.gen.coroutine
def push_message(account_id, content, header=None):

    if content is None:
        LOGGER.info("content is None.")
        raise HTTPError(500, "internal error. content is None.")

    request = {
        "accountId": account_id,
        "content": content
    }

    headers = API_BO["headers"]
    if header is not None:
        headers = Merge(header, headers)

    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["push_url"]
    url = replace_url_bot_no(url)
    response = auth_post(url, data=json.dumps(request), headers=headers)
    if response.status_code != 200:
        LOGGER.error("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise HTTPError(500, "internal error. Internal interface call error.")


@tornado.gen.coroutine
def push_messages(account_id, contents):

    if contents is None:
        LOGGER.info("contents is None.")
        raise HTTPError(500, "internal error. contents is None.")

    for content in contents:
        yield push_message(account_id, content)
