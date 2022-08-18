import time
import csv
import os
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Logger:
    def __init__(self, csvColumns, log_id=time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())):
        self.id = log_id
        self.intervalInSeconds = 1
        self.csvFileColumns = csvColumns

        self.data = {}

        os.makedirs(self.getLogsFolderPath(), exist_ok=True)

    @staticmethod
    def lastLog(csvColumns):
        last_log_filename = sorted(os.listdir('logs/'))[-1]
        last_log_id = os.path.splitext(last_log_filename)[0]
        print(last_log_id)
        return Logger(csvColumns, log_id=last_log_id)

    def getLogsFolderPath(self):
        return 'logs'

    def getFilePath(self):
        return f'{self.getLogsFolderPath()}/{self.id}.csv'

    def updateData(self, data):
        self.data = data

    def startLoggingData(self):
        if not (hasattr(self, 'csvfile') and hasattr(self, 'dictwriter')):
            self.csvfile = open(self.getFilePath(), 'w', newline='')
            self.dictwriter = csv.DictWriter(self.csvfile, self.csvFileColumns, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.dictwriter.writeheader()

            self.thread = RepeatTimer(self.intervalInSeconds, self.logData)
            self.thread.start()
    
    def logData(self):
        self.dictwriter.writerow(self.data)

    def endLogging(self):
        if hasattr(self, 'csvfile') and hasattr(self, 'dictwriter'):
            self.thread.cancel()
            self.csvfile.close()
            delattr(self, 'csvfile')
            delattr(self, 'dictwriter')

    def getRows(self):
        csvfile = open(self.getFilePath(), newline='')
        dictreader = csv.DictReader(csvfile, self.csvFileColumns, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        rows = [row for row in dictreader]
        # remove header
        rows = rows[1:]
        csvfile.close()
        return rows
