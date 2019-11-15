#!/bin/env bash

# supervisord and calendar_bot logs are auto cleaned.
# see the configure files for them.

# remove out of date calendar_bot logs and compress log
clover_log_path=/home1/irteam/logs/calendar_bot/
find $calendar_bot_log_path -mtime +50 -name 'calendar_bot.log.*.xz' -delete
find $calendar_bot_log_path -name 'calendar_bot.log.*-*' -not -name 'calendar_bot.log.*.xz' -execdir xz -z -T4 {} \;
