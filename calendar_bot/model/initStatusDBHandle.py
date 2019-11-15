#!/bin/env python
# -*- coding: utf-8 -*-
import logging
from calendar_bot.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable


def insert_init_status(action, extra):
    insert_sql = "INSERT INTO system_init_status(action, extra) " \
                 "VALUES('%s', '%s') ON CONFLICT(action) " \
                 "DO UPDATE SET extra='%s', update_time=now()" % \
                 (action, extra, extra)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(insert_sql)


def update_init_status(action, extra):
    update_sql = "UPDATE system_init_status SET update_time=now()," \
                 "extra='%s' " \
                 "WHERE action='%s'" % (extra, action)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(update_sql)


def get_init_status(action):
    select_sql = "SELECT extra " \
                 "FROM system_init_status WHERE action='%s'" % (action,)

    extra = None
    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) == 1:
            extra = rows[0][0]
    return extra


def delete_init_status(action):
    select_sql = "DELETE FROM system_init_status WHERE action='%s'" % (action,)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
