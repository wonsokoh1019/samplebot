#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import json
import logging
import tornado.web
from calendar_bot.check_and_handle_actions import CheckAndHandleActions

LOGGER = logging.getLogger("calendar_bot")


class CallbackHandler(tornado.web.RequestHandler):
    """
    /internal/hello
    """

    @tornado.gen.coroutine
    def post(self):
        """
        support post
        """

        LOGGER.info("request para path:%s", self.request.uri)
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            LOGGER.exception('Failed parse json:%s' % self.request.body)
            raise tornado.web.HTTPError(403, "boy is not json.")

        LOGGER.info("request para body:%s", self.request.body)
        checker = CheckAndHandleActions()
        yield checker.execute(body)

        self.finish()
