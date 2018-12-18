from Command import Command
from iExecLog import Log
import re


class Order():
    id = "none"
    price = "None"
    pool = "None"
    category = "None"
    timestamp = "None"

    def __init__(self, _id=None, _price=None, _pool=None, _category=None, _timestamp=None):
        self.id = _id
        self.price = _price
        self.pool = _pool
        self.category = _category
        self.timestamp = _timestamp

    def show(self):
        return [self.id, self.price, self.pool, self.category, self.timestamp]

    def set(self, _id, _price, _pool, _category, _timestamp):
        self.id = _id
        self.price = _price
        self.pool = _pool
        self.category = _category
        self.timestamp = _timestamp


Status = {"Started", "Error", "Completed"}


class Work():
    tx = "none"
    id = "None"
    status = "None"

    def __init__(self, tx=None, id=None, status=None):
        self.tx = tx
        self.id = id
        self.status = status

    def show(self):
        return [self.tx, self.id, self.status]

    def set(self, tx, id, status):
        self.tx = tx
        self.id = id
        self.status = status


class Orderlist():

    def __init__(self, cat, nbworks=1, simulate=False, log=False, logfile=None):
        self.cat = cat
        self.book = []
        self.works = []
        self.nbworks = nbworks
        self.nbworkssubmitted = 0
        self.simulate = simulate
        self.log = Log(log=log, logfile=logfile)
        self.log.add("Start program to launch " + str(self.nbworks) + "works ")

    def update(self):
        self.book = []
        _found_allcat = 0
        for _cat in self.cat:
            cmd = "iexec orderbook show --category " + str(_cat)
            ret = Command(cmd).run2()
            current_cat = self.fill_ob(ret.output)
            self.log.add(str(current_cat) + " order(s) found in cat " + str(_cat))
        self.log.add(str(_found_allcat) + " order(s) found")

    def fill_ob(self, input):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        tmp = ansi_escape.sub('', input)
        _list = tmp.split()
        idx = 0
        _found = 0
        while idx < len(_list):
            if _list[idx] == "id:":
                _firstorder = Order()
                _firstorder.set(_list[idx + 1], _list[idx + 3], _list[idx + 5], _list[idx + 7], _list[idx + 9])
                idx += 10
                self.book.append(_firstorder)
                _found += 1
            idx += 1
        return _found

    def submit(self):
        for order in self.book:
            self.log.add("try to buy this order" + str(order.show()))
            _work = self.submitorder(order.id)
            if _work.status == "Started":
                self.works.append(_work)
                self.nbworkssubmitted += 1
                print("https://explorer.iex.ec/kovan/work/" + _work.tx)
                self.log.add("work is " + str(_work))
                if self.nbworkssubmitted >= self.nbworks:
                    self.log.add("all task has been succesfully submitted ... exit ")
                    self.close()

    def submitorder(self, _orderid):
        cmd = "iexec order fill " + _orderid + " --force"
        if not self.simulate:
            result = Command(cmd).run()
            # self.log.add("[[[[[" + result.error + result.output +" ]]]]]]")
            work = self.watch(result.error + result.output, _orderid)
            if work.status == "Error":
                self.log.add("!!! submission error " + str(_orderid))
            elif work.status == "Started":
                self.log.add("\o/ successful  work submission " + str(_orderid))
            else:
                self.log.add("[[[[[" + result.error + result.output + " ]]]]]]")
                raise RuntimeError
        else:
            work = Work(status="Started")
            self.log.add("Simulate:  " + cmd)
        return work

    def show(self):
        self.log.add("orderlist is ")
        for i in self.book:
            self.log.add(str(i.show()))

    def watch(self, txt, orderid):
        if "is already closed and so cannot be filled. " in txt:
            self.log.add("problem found in " + str(orderid) + " cannot be filled")
            work = Work(tx=-1, id=orderid, status="Error")
        elif "failed with Error" and "iexec.json" and "did you forget to run " in txt:

            work = Work(tx=-1, id=orderid, status="Error")
        elif "failed with Error" and " [ethjs-query] while formatting outputs from RPC" \
                and "Transaction nonce is too low. Try incrementing the nonce." in txt:
            self.log.add("problem found in " + str(orderid) + " Transaction nonce is too low")
            work = Work(tx=-1, id=orderid, status="Error")
        elif "failed with Error" and "Transaction gas price is too low" \
                and "Try increasing the gas price or incrementing the nonce" in txt:
            self.log.add("problem found in " + str(orderid) + " Transaction gas price or nonce is too low")
            work = Work(tx=-1, id=orderid, status="Error")
        elif "TypeError: Converting circular structure to JSON" \
                and "This error originated either by throwing inside of an async function without a catch block" in txt:
            self.log.add("problem found in " + str(orderid) +
                  " This error originated either by throwing inside of an async function without a catch block")
            work = Work(tx=-1, id=orderid, status="Error")
        else:
            if re.search(r'New work at \s*([^\n]+)', txt) is None:
                self.log.add("((((" + txt + "))))")
                raise Exception('This is broken')
            else:
                workid = re.search(r'New work at \s*([^\n]+)', txt).group(1).split()[0]
                self.log.add("work id found is " + str(workid))
                self.log.add("work submitted ethereum " + str(workid) + "orderid is " + str(orderid) + " "
                      + str(self.nbworkssubmitted+1) + "/" + str(self.nbworks))
                work = Work(tx=str(workid), id=orderid, status="Started")
        self.log.add("work is " + str(work.show()))
        return work

    def close(self):
        self.log.add("close program")
        self.log.close()
        # exit with no error
        exit(0)
