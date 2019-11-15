#!/bin/bash python
# -*- coding: utf-8 -*-
"""
launch calendar_bot
"""

__all__ = ['sig_handler', 'kill_server', 'init_logger', 'check_init_bot',
           'init_rich_menu_first', 'init_calendar_first', 'start_calendar_bot']

import os
import logging
from logging import StreamHandler
import asyncio
import uvloop
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
from calendar_bot.externals.richmenu import init_rich_menu
from calendar_bot.common import global_data
from calendar_bot.externals.calendar_req import init_calendar
from calendar_bot.constant import API_BO
from calendar_bot.model.initStatusDBHandle import insert_init_status, \
    get_init_status

import psutil

import calendar_bot.router
import calendar_bot.contextlog
from calendar_bot.settings import CALENDAR_PORT, CALENDAR_LOG_FMT, \
    CALENDAR_LOG_LEVEL, CALENDAR_LOG_FILE, CALENDAR_LOG_ROTATE

define("port", default=CALENDAR_PORT, help="server listen port. "
                                           "default 8080")
define("workers", default=0, help="the count of workers. "
                                  "default the same as cpu cores")
define("logfile", default=None, help="the path for log")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def sig_handler(sig, _):
    """
    signal handler
    """
    print("sig %s received" % str(sig))
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children()
        for process in children:
            process.send_signal(sig)
    except (psutil.NoSuchProcess, psutil.ZombieProcess,
            psutil.AccessDenied) as ex:
        print(str(ex))
    tornado.ioloop.IOLoop.instance().add_callback(kill_server)


def kill_server():
    """
    stop the ioloop
    """
    asyncio.get_event_loop().stop()


def init_logger():
    """
    Initializes the logger settings.
    """
    formatter = logging.Formatter(CALENDAR_LOG_FMT)
    calendar_log = logging.getLogger("calendar_bot")
    file_handler = StreamHandler()
    file_handler.setFormatter(formatter)

    calendar_log.setLevel(CALENDAR_LOG_LEVEL)
    file_handler.addFilter(calendar_bot.contextlog.RequestContextFilter())
    calendar_log.addHandler(file_handler)

    logging.getLogger("tornado.application").addHandler(file_handler)
    logging.getLogger("tornado.general").addHandler(file_handler)


def check_init_bot():
    """
    Initialize bot no, check if the bot is initialized.
    If this function gets an exception, it is probably like script/registerBot.py.
    This is not executed or the execution failed.
    ref: https://developers.worksmobile.com/jp/document/3005001?lang=en
    """
    extra = get_init_status("bot_no")
    if extra is None:
        raise Exception("bot no init failed.")
    global_data.set_value("bot_no", extra)


def init_rich_menu_first():
    """
    Initialize rich menu API. Check also: calendar_bot/externals/richmenu.py
    ref: https://developers.worksmobile.com/jp/document/1005040?lang=en
    """
    rich_menu_id = get_init_status("rich_menu")

    if rich_menu_id is None:
        rich_menu_id = init_rich_menu()
        insert_init_status("rich_menu", rich_menu_id)

    if rich_menu_id is None:
        raise Exception("init rich menu failed.")
    global_data.set_value("rich_menu", rich_menu_id)


def init_calendar_first():
    """
    Initialize calendar API.
    """
    calendar_id = get_init_status("calendar")
    if calendar_id is None:
        calendar_id = init_calendar()
        insert_init_status("calendar", calendar_id)

    global_data.set_value(API_BO["calendar"]["name"], calendar_id)


def start_calendar_bot():
    """
    the calendar_bot launch code

    tornado.httpserver a non-blocking, single-threaded HTTP server
    ref: https://www.tornadoweb.org/en/stable/httpserver.html

    tornado.routing flexible routing implementation.
    ref: https://www.tornadoweb.org/en/stable/routing.html

    If you use the event loop that comes with tornado, many third-party
    packages based on asyncio may not be used, such as aioredis.
    """

    server = tornado.httpserver.HTTPServer(calendar_bot.router.getRouter())

    server.bind(options.port)
    server.start(1)

    init_logger()
    check_init_bot()
    init_rich_menu_first()
    init_calendar_first()

    asyncio.get_event_loop().run_forever()
    server.stop()
    asyncio.get_event_loop().close()

    print("exit...")
