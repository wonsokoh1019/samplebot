#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import psycopg2
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable, DuplicateObject
sys.path.append('./')
from calendar_bot.constant import DB_CONFIG


# create calendar table
def create_calendar_table():
    create_sql = '''
                CREATE TABLE IF NOT EXISTS bot_calendar_record( 
                 schedule_id  varchar(128)      NOT NULL, 
                 account      varchar(64)       NOT NULL, 
                 cur_date     date              NOT NULL, 
                 begin_time   bigint            NOT NULL, 
                 end_time     bigint            NOT NULL, 
                 create_time  timestamp         NOT NULL 
                 default current_timestamp, 
                 update_time  timestamp         NOT NULL 
                 default current_timestamp, 
                 PRIMARY KEY (schedule_id));
                 '''

    index_sql = '''CREATE UNIQUE INDEX account_time 
                ON bot_calendar_record(account, cur_date);'''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(create_sql)
                cur.execute(index_sql)
            except DuplicateTable:
                pass

# create init status table
def create_init_status():
    create_sql = ''' 
                CREATE TABLE IF NOT EXISTS system_init_status( 
                 action       varchar(64)   NOT NULL, 
                 extra      varchar(128)     DEFAULT NULL, 
                 create_time  TIMESTAMP     NOT NULL 
                 DEFAULT      CURRENT_TIMESTAMP, 
                 update_time  TIMESTAMP         NOT NULL 
                 default      CURRENT_TIMESTAMP, 
                 PRIMARY KEY (action));
                '''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)

# create status tables
def create_process_status_table():
    status_type_sql = '''
                        CREATE TYPE m_status AS  
                            ENUM('none', 'wait_in', 'in_done', 
                            'wait_out', 'out_done');
                      '''

    process_type_sql = '''
                        CREATE TYPE m_process AS 
                           ENUM('none', 'sign_in_done', 'sign_out_done');
                       '''

    create_sql = '''
                CREATE TABLE IF NOT EXISTS bot_process_status( 
                 account      varchar(64)   NOT NULL,  
                 cur_date     date          NOT NULL,  
                 status       m_status      DEFAULT NULL,  
                 process      m_process     DEFAULT NULL,  
                 create_time  timestamp     NOT NULL  
                 default current_timestamp,  
                 update_time  timestamp         NOT NULL  
                 default current_timestamp, 
                 PRIMARY KEY (account, cur_date));
                 '''

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(status_type_sql)
                cur.execute(process_type_sql)
                cur.execute(create_sql)
            except DuplicateObject:
                print("bot_process_status is DuplicateObject. please check it.")
                pass
            except DuplicateTable:
                pass

def main():
    create_calendar_table()
    create_init_status()
    create_process_status_table()

if __name__ == "__main__":
    main()
