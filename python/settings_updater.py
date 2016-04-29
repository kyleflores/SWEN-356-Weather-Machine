import json, sys
import cron_jobs

class SettingsUpdater:

    def __init__(self):
        data = json.load(sys.stdin)
        updateFile(data)

    def updateFile(self, data):
        settingsFile = '../www/html/json/settings.json'
        fileWriter = open(data_file, 'w')

        #empty the file before writing
        fileWriter.seek(0)
        fileWriter.truncate()

        #write the updated JSON to the file and close it.
        fileWriter.write(data)
        fileWriter.close()

def main():
    #do json writing here
    #cron_jobs.reset_alarms()
    #f = open('/home/pi/test.output','w')
    #f.write("hello world")
    #f.close()

main()
