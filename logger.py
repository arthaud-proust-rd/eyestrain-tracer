import time
import csv
import os
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Logger:
    def __init__(self, csvColumns):
        self.id = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
        self.intervalInSeconds = 1
        self.csvFileColumns = csvColumns

        self.data = {}

        os.makedirs(self.getLogsFolderPath(), exist_ok=True)

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