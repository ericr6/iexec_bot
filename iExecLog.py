from datetime import datetime


class Log(object):
    def __init__(self, filename):
        self.filename = filename
        self.f = open(filename, "a")

    def add(self, txt, showdate=True):
        now = datetime.now()
        if showdate is True:
            self.f.write("[" + now.strftime("%H:%M:%S.%f") + "]  " + txt + "\n")
        else:
            self.f.write(txt + "\n")
        self.f.flush()

    def close(self):
        self.f.close()

