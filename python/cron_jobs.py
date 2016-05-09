#!/usr/bin/env python3

from crontab import CronTab
from datetime import datetime
import json

CRONTAB_FILE = "/etc/crontab"
NOTIFICATION_USER = "pi"
NOTIFICATION_COMMENT = "weather machine notification"
NOTIFICATION_COMMAND = NOTIFICATION_USER + " python3 /home/" + \
    NOTIFICATION_USER + "/SWEN-356-Weather-Machine/python/notify.py " 
JSON_SETTINGS_FILE = "/home/pi/SWEN-356-Weather-Machine/www/html/json/settings.json"

ALARM_VERBOSITY = {
    0:'0',
    1:'1',
    2:'2'
    }

def reset_alarms():
    cron = CronTab(tabfile=CRONTAB_FILE)
    cron.remove_all(comment=NOTIFICATION_COMMENT)
    job = None
    for alarm in get_alarms():
        job = cron.new(command=NOTIFICATION_COMMAND + str(alarm[1]),\
            comment=NOTIFICATION_COMMENT, user=True)
        job.hour.on(alarm[0].hour)
        job.minute.on(alarm[0].minute)
    cron.write()

def get_alarms():
    settings_file = open(JSON_SETTINGS_FILE).read()
    json_data = json.loads(settings_file)
    alarms = []
    verbosity = 0
    time = None
    for alarm in json_data:
        verbosity = ALARM_VERBOSITY[alarm['alarm']['priority']]
        time = datetime.strptime(alarm['alarm']['time'],"%H:%M:%S")
        alarms.append((time,verbosity))
    return alarms

reset_alarms()
