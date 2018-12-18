#!/usr/bin/env python
import sys
import time
from Argparser import Argparser
from Order import Orderlist

if __name__ == "__main__":

    # Parsing Options
    parser = Argparser(sys.argv[1:])
    info = parser.get_info()

    # init
    orderbook = Orderlist(info["category"], nbworks=info["nbtasks"], simulate=info["simulate"],
                          log=info["log"], logfile=info["logfile"])
    while 1:
        orderbook.update()
        orderbook.submit()
        time.sleep(info["pollingtime"])

