from crontab import CronTab
from datetime import time

CRONTAB_FILE = "/etc/crontab"
NOTIFICATION_USER = "pi"
NOTIFICATION_COMMENT = "weather machine notification"
NOTIFICATION_COMMAND = NOTIFICATION_USER + " python3 /home/" + \
    NOTIFICATION_USER + "/SWEN-356-Weather-Machine/python/notify.py " 

def reset_alarms():
    #will be run from weather_machine.py
    cron = CronTab(CRONTAB_FILE)
    cron.remove_all(comment=NOTIFICATION_COMMENT)
    job = None
    for alarm in get_alarms():
        job = cron.new(command=NOTIFICATION_COMMAND + alarm[1],\
            comment=NOTIFICATION_COMMENT)
        job.hour.on(alarm[0].hour)
        job.minute.on(alarm[0].minute)
    cron.write()

def get_alarms():
    #read from json file
    #will return array of tuples with the following setup
    #time, importance
    return [(,),]
