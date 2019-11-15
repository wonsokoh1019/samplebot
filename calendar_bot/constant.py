#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os
from conf.config import *
# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------

# root path
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)

SERVICE_CONSUMER_KEY = None
HEROKU_SERVER_ID = SERVER_ID
IP_TOKEN = TOKEN
PRIVATE_KEY_PATH = ABSDIR_OF_PARENT + "/key/" + PRIVATE_KEY_NAME

# domain
STORAGE_DOMAIN = "alpha-storage.worksmobile.com"
AUTH_DOMAIN = "alpha-auth.worksmobile.com"
DEVELOP_API_DOMAIN = "alpha-apis.worksmobile.com"

# RICH_MENUS
RICH_MENUS = {
                "name": "calendar_bot_rich_menu_en",
                "path": ABSDIR_OF_PARENT + "/image/en/Rich_Menu.png"
             }

# IMAGE CAROUSEL
IMAGE_CAROUSEL = {
                    "resource_url":
                    [
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_01.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_02.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_03.png"
                    ]
                }

# API
API_BO = {
            "headers": {
                "content-type": "application/json",
                "charset": "UTF-8"
            },
            "upload_url": "http://" + STORAGE_DOMAIN
                          + "/openapi/message/upload.api",
            "push_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                        + API_ID + "/message/v1/bot/_BOT_NO_/message/push",
            "rich_menu_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                             + API_ID + "/message/v1/bot/_BOT_NO_/richmenu",

            "calendar":
            {
                "name": "calendar bot",
                "create_calendar_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_EXTERNAL_KEY_/"
                                       "calendarList",
                "create_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_EXTERNAL_KEY_/calendars/"
                                       "_CALENDAR_ID_/events",
                "modify_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_EXTERNAL_KEY_/calendars/"
                                       "_CALENDAR_ID_/events/_CALENDAR_UUID_",
            },

            "TZone":
            {
                "external_key_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                    + API_ID
                                    + "/contact/getDomainContact/v1?"
                                      "account=" + ADMIN_ACCOUNT,
                "time_zone_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                 + API_ID
                                 + "/organization/v2/domains/DOMAIN_ID"
                                   "/users/EXTERNAL_KEY/g11ns"
            },
            "auth_url": "https://" + AUTH_DOMAIN + "/b/" + API_ID
                        + "/server/token?grant_type=urn%3Aietf%3Aparams%3Aoauth"
                          "%3Agrant-type%3Ajwt-bearer&assertion="
        }

OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": CONSUMER_KEY,
        "service_consumerKey": SERVICE_CONSUMER_KEY
    }

# DB
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "sslmode": DB_SSLMODE
}

# FILE SYSTEM
FILE_SYSTEM = {
    "image_dir": ABSDIR_OF_PARENT+"/image",
}
