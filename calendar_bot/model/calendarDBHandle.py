#!/bin/env python
# -*- coding: utf-8 -*-
import logging
from calendar_bot.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable

LOGGER = logging.getLogger("calendar_bot")

# inset schedule
def set_schedule_by_user(schedule_id, account, date,  begin, end):
    insert_sql = "INSERT INTO bot_calendar_record(schedule_id, account, " \
                 "cur_date, begin_time, end_time) " \
                 "VALUES('%s', '%s', '%s', %d, %d)" \
                 % (schedule_id, account, date, begin, end)

    post_gre = PostGreSql()

    with post_gre as cursor:
        cursor.execute(insert_sql)


# update schedule
def get_schedule_by_user(account, date):
    select_sql = "SELECT schedule_id, begin_time " \
                 "FROM bot_calendar_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    row = None
    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) == 1:
            # ["schedule_id", "begin_time"]
            row = rows[0]
    return row


def modify_schedule_by_user(schedule_id, end):
    select_sql = "UPDATE bot_calendar_record " \
                 "SET end_time=%d, update_time=now()" \
                 "WHERE schedule_id='%s'" \
                 % (end, schedule_id)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)


def clean_schedule_by_user(account, date):
    delete_sql = "DELETE FROM bot_calendar_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(delete_sql)
