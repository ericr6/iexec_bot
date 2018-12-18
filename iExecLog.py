from datetime import datetime


class Log(object):
    def __init__(self, log, logfile):
        self.filename = logfile
        self.log = log
        if self.log:
            self.f = open(str(logfile), "a")

    def add(self, txt, showdate=True):
        now = datetime.now()
        if self.log:
            if showdate is True:
                self.f.write("[" + now.strftime("%H:%M:%S.%f") + "]  " + txt + "\n")
            else:
                self.f.write(txt + "\n")
            self.f.flush()

    def close(self):
        if self.log:
            self.f.close()

