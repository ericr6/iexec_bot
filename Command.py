import subprocess


class Command(object):
    """Run a command and capture it's output string, error string and exit status"""

    def __init__(self, command):
        self.output = ""
        self.error = ""
        self.failed = ""
        self.command = command

    # Blocking start with immediate stdout expectation
    def run(self):
        import subprocess as sp
        process = sp.Popen(self.command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
        self.output, self.error = process.communicate()
        if self.output is None:
            print(self.error)
        self.failed = process.returncode
        return self

    def run2(self):
        import subprocess as sp
        process = sp.Popen(self.command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
        self.output, self.error = process.communicate()
        self.output = self.error + self.output
        self.failed = process.returncode
        return self


