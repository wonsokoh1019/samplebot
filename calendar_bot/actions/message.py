# !/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from calendar_bot.model.data import make_i18n_label, make_message_action, \
    i18n_display_text, make_postback_action, \
    make_quick_reply_item, i18n_text, make_text
from calendar_bot.constant import API_BO, IMAGE_CAROUSEL, RICH_MENUS
from calendar_bot.common.local_timezone import local_date_time

LOGGER = logging.getLogger("calendar_bot")


class TimeStruct:
    def __init__(self, sign_time):
        self.date_time = local_date_time(sign_time)

        self.month = str(self.date_time.month)
        self.date = str(self.date_time.day)
        self.min = str(self.date_time.minute)

        self.interval_en = "AM"

        self.hours = str(self.date_time.hour)
        if self.date_time.hour > 12:
            self.interval_en = "PM"
            self.hours = str(self.date_time.hour - 12)

        self.str_current_time_tick = str(sign_time)
        pos = self.str_current_time_tick.find(".")
        if pos != -1:
            self.str_current_time_tick = self.str_current_time_tick[:pos]


def create_button_actions(direct_sign_callback, manual_sign_callback):
    action1 = make_message_action("Current time", direct_sign_callback)
    action2 = make_message_action("Manually enter", manual_sign_callback)

    return [action1, action2]


def create_quick_replay_items(confirm_callback, previous_callback):

    action1 = make_postback_action(confirm_callback,
                                   label="yes", display_text="yes",)
    reply_item1 = make_quick_reply_item(action1)

    action2 = make_postback_action(previous_callback,
                                   label="No", display_text="No")
    reply_item2 = make_quick_reply_item(action2)

    return [reply_item1, reply_item2]


def prompt_input():
    return make_text(
        "Please use the military time format "
        "with a total of 4 numerical digits (hhmm) "
        "when entering the time."
        "For example, type 2020 to indicate 8:20 PM. ")


def number_message():

    text1 = make_text("You have created your leave time "
                      "earlier than your leave time. "
                      "Please check your work time and enter again.")

    text2 = prompt_input()
    return [text1, text2]


def error_message():
    text1 = make_text("Sorry, but unable to "
                      "comprehend your composed time. "
                      "Please check the time entry method again, "
                      "and enter the time.")

    text2 = prompt_input()
    return [text1, text2]


def invalid_message():
    return make_text("I didn't understand the text. "
                     "When you go to work or go home, "
                     "Please select the appropriate "
                     "\"Record\" button for each.")


def reminder_message(process):
    text = None
    if process == "sign_in_done":
        text = make_text("There is already a clock-in time. "
                         "Please select \"Record\" on the "
                         "bottom of the menu when you clock out.")

    elif process == "sign_out_done":
        text = make_text("There is already a clock-out time."
                         "Please select \"Record\" on the bottom "
                         "of the menu when you clock in.")
    elif process is None:
        text = make_text("Today's clock-in time has not been registered. "
                         "Please select \"Record clock-in\" on the bottom "
                         "of the menu, and enter your clock-in time.")
    return text
