import unittest
from Command import Command
from Order import Order, Orderlist
import re, json


def broken_function():
    raise Exception('This is broken')


class TestStringMethods(unittest.TestCase):

    def test(self):
        with self.assertRaises(Exception) as context:
             broken_function()
        self.assertTrue('This is broken' in str(context.exception))

    def test_get_failed_submission(self):
        with self.assertRaises(Exception) as context:
            intext = """bullshit"""
            test = Orderlist(cat=[3, 4, 5])
            test.watch(intext, 1)
            test.log.close()
        self.assertTrue(('This is broken' in str(context.exception)))

    def test_fail_gas(self):
        intext= """    ℹ
    iExec     SDK     update    available     2.2    .39 →  2.3    .1, Run    "npm -g i iexec"    to
    update

    ℹ
    using
    chain[kovan]
    - filling    order...
    ℹ    app    price: 2    nRLC    for app 0x4d3a21f38Faf0C0C07F738796b440Ff31E244eF2
        ℹ
        workerpool
        price: 1565
        nRLC
  for workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
ℹ
  work
  parameters:
 cmdline: -l
 zec - eu1.nanopool.org: 6666 - u
 t1JmoxkLcdvbLsfUbTKm3CSsC8fyeFvUeRM - p
 x

 - filling
 order...
 ✖ command
 "iexec order fill"
 failed
 with Error:
  [ethjs - query]
 while formatting outputs from RPC '{"value":{"code":-32010,"message":"Transaction gas price is too low. There is another transaction with same nonce in the queue. Try increasing the gas price or incrementing the nonce."}}'

 Usage: iexec - order[options][command]

 Options:
 -h, --help
 output
 usage
 information


Commands:
init[options]
init
a new order place[options] place a new order fill[options] < orderID > fill
an order to execute a work cancel[options] < orderID > cancel
an order show[options] < orderID > show marketplace order details count[options] get marketplace order count

Links:

doc: https: // github.com / iExecBlockchainComputing / iexec - sdk  # iexec-sdk-api
bugs: https: // github.com / iExecBlockchainComputing / iexec - sdk / issues
help: https: // slack.iex.ec
"""
        test = Orderlist(cat=[5])
        work = test.watch(intext, 1)
        test.log.close()
        self.assertEqual(work.status, "Error")

    def test_find_error_sdcbsqjdbj(self):
        intext="""
ℹ iExec SDK update available 2.2.39 →  2.3.1, Run "npm -g i iexec" to update

ℹ using chain [kovan]
- filling order...
(node:10336) UnhandledPromiseRejectionWarning: TypeError: Converting circular structure to JSON
    at JSON.stringify (<anonymous>)
    at /usr/lib/node_modules/iexec/node_modules/ethjs-query/lib/index.js:108:99
    at <anonymous>
    at process._tickCallback (internal/process/next_tick.js:189:7)
(node:10336) UnhandledPromiseRejectionWarning: Unhandled promise rejection.
 This error originated either by throwing inside of an async function without a catch block,
 or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:10336) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections
 that are not handled will terminate the Node.js process with a non-zero exit code.
(node:10336) UnhandledPromiseRejectionWarning: TypeError: Converting circular structure to JSON
    at JSON.stringify (<anonymous>)
    at /usr/lib/node_modules/iexec/node_modules/ethjs-query/lib/index.js:108:99
    at <anonymous>
    at process._tickCallback (internal/process/next_tick.js:189:7)
(node:10336) UnhandledPromiseRejectionWarning: Unhandled promise rejection.
 This error originated either by throwing inside of an async function without a catch block,
  or by rejecting a promise which was not handled with .catch(). (rejection id: 2)

"""
        test = Orderlist(cat=[5])
        work = test.watch(intext, 1)
        test.log.close()
        self.assertEqual(work.status, "Error")

    def test_get_successfull_occu(self):
        intext = """ ℹ iExec SDK update available 2.2.39 →  2.3.0, Run "npm -g i iexec" to update

     ℹ using chain [kovan]
     ℹ app price: 2 nRLC for app 0x4d3a21f38Faf0C0C07F738796b440Ff31E244eF2
     ℹ workerpool price: 1037 nRLC for workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
     ℹ work parameters:
     cmdline: -l zec-eu1.nanopool.org:6666 -u t1JmoxkLcdvbLsfUbTKm3CSsC8fyeFvUeRM -p x

     ✔ Filled order with ID 1555
     ✔ New work at 0x2216e38fe2a51be4187a0f267745d3b2d726f728 submitted to workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
             """
        test = Orderlist(cat=[5])
        work = test.watch(intext, 1)
        test.log.close()
        self.assertEqual(work.tx, "0x2216e38fe2a51be4187a0f267745d3b2d726f728")

    def test_create_orderlist(self):
        input = """
         ['ℹ', 'iExec', 'SDK', 'update', 'available', '2.2.39', '→', '2.3.1,', 'Run', '"npm', '-g', 'i', 'iexec"', 'to',
        'update', 'ℹ', 'using', 'chain', '[kovan]', '-', 'showing', 'orderbook...', '✔', 'orderbook', 'details:',
        '\x1b[32m-', '\x1b[39m', '\x1b[32mid:', '\x1b[39m', '1633', '\x1b[32mprice:', '\x1b[39m', '13200', '\x1b[32mpool:',
         '\x1b[39m', '0x49327538C2f418743E70Ca3495888a62B587A641', '\x1b[32mcategory:', '\x1b[39m', '5',
         '\x1b[32mtimestamp:', '\x1b[39m2018-12-13T10:34:48.000Z', '\x1b[32m-', '\x1b[39m', '\x1b[32mid:', '\x1b[39m',
         '1328', '\x1b[32mprice:', '\x1b[39m', '15336', '\x1b[32mpool:', '\x1b[39m',
         '0x49327538C2f418743E70Ca3495888a62B587A641', '\x1b[32mcategory:', '\x1b[39m', '5', '\x1b[32mtimestamp:',
         '\x1b[39m2018-11-13T14:19:44.000Z', '\x1b[32m-', '\x1b[39m', '\x1b[32mid:', '\x1b[39m', '1628', '\x1b[32mprice:',
         '\x1b[39m', '16395', '\x1b[32mpool:', '\x1b[39m', '0x0061B8b1191394FA710Def946368675B79DB062b',
         '\x1b[32mcategory:', '\x1b[39m', '5', '\x1b[32mtimestamp:', '\x1b[39m2018-12-12T18:41:40.000Z', '\x1b[32m-',
         '\x1b[39m', '\x1b[32mid:', '\x1b[39m', '1340', '\x1b[32mprice:', '\x1b[39m', '17024', '\x1b[32mpool:', '\x1b[39m',
         '0x49327538C2f418743E70Ca3495888a62B587A641', '\x1b[32mcategory:', '\x1b[39m', '5', '\x1b[32mtimestamp:',
         '\x1b[39m2018-11-15T14:11:40.000Z', '\x1b[32m-', '\x1b[39m', '\x1b[32mid:', '\x1b[39m', '1615', '\x1b[32mprice:',
         '\x1b[39m', '18128', '\x1b[32mpool:', '\x1b[39m', '0x49327538C2f418743E70Ca3495888a62B587A641',
         '\x1b[32mcategory:', '\x1b[39m', '5', '\x1b[32mtimestamp:', '\x1b[39m2018-12-12T10:32:36.000Z', 'ℹ', 'trade', 'in',
         'the', 'browser', 'at', 'https://market.iex.ec']"""

        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        newtext = ansi_escape.sub('', input)
        self.assertEqual("1", "1")

    def test_get_successfull_fill(self):
        intext = """ ℹ iExec SDK update available 2.2.39 →  2.3.0, Run "npm -g i iexec" to update

    ℹ using chain [kovan]
    ℹ app price: 2 nRLC for app 0x4d3a21f38Faf0C0C07F738796b440Ff31E244eF2
    ℹ workerpool price: 1037 nRLC for workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
    ℹ work parameters:
    cmdline: -l zec-eu1.nanopool.org:6666 -u t1JmoxkLcdvbLsfUbTKm3CSsC8fyeFvUeRM -p x

    ✔ Filled order with ID 1555
    ✔ New work at 0x2216e38fe2a51be4187a0f267745d3b2d726f728 submitted to workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
            """

        workid = re.search(r'New work at \s*([^\n]+)', intext).group(1).split()[0]

        self.assertEqual(workid, "0x2216e38fe2a51be4187a0f267745d3b2d726f728")

    def test_get_successfull_occu2(self):
        intext = """ ℹ iExec SDK update available 2.2.39 →  2.3.0, Run "npm -g i iexec" to update

    ℹ using chain [kovan]
    ℹ app price: 2 nRLC for app 0x4d3a21f38Faf0C0C07F738796b440Ff31E244eF2
    ℹ workerpool price: 1037 nRLC for workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
    ℹ work parameters:
    cmdline: -l zec-eu1.nanopool.org:6666 -u t1JmoxkLcdvbLsfUbTKm3CSsC8fyeFvUeRM -p x

    ✔ Filled order with ID 1555
    ✔ New work at 0x2216e38fe2a51be4187a0f267745d3b2d726f728 submitted to workerpool 0x851f65b27030ac9634bf514ffbc3c1369ed747e9
            """
        test = Orderlist(cat=[3, 4, 5])
        work = test.watch(intext, 1)
        test.log.close()
        self.assertEqual(work.tx, "0x2216e38fe2a51be4187a0f267745d3b2d726f728")

    def test_detect_an_error_when_an_order_is_submitted(self):
        # cmd = "iexec order fill 1328 --force", result = Command(cmd).run()
        _errlog = """ℹ iExec SDK update available 2.2.39 →  2.3.0, Run "npm -g i iexec" to update

    ℹ using chain [kovan]
    - filling order...
    ✖ command "iexec order fill" failed with Error: order with ID 1328 is already closed and so cannot be filled. 
     You could run "iexec order show 1328" for more details
    """
        test = Orderlist(cat=[3, 4, 5])
        work = test.watch(_errlog, 1)
        test.log.close()
        self.assertTrue(work.tx, "Error")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_call(self):
        cmd = "echo $USER"
        result = Command(cmd).run()
        self.assertEqual(result.output, 'eric\n')

    def test_iexec(self):
        cmd = "iexec --version"
        result = Command(cmd).run()
        self.assertEqual(result.output, '2.3.1\n')

    def test_find_nb_order_orderbook(self):
        intext="""('', 'ℹ using chain [kovan]\n- showing orderbook...\n✔ orderbook details:\n- \n  id:
                1432\n  price:     15270\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n 
          category:  5\n  timestamp: 2018-11-29T17:28:24.000Z\n- \n  id:        1328\n  price:   
          15336\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n 
          timestamp: 2018-11-13T14:19:44.000Z\n- \n  id:        1401\n  price:     15743\n
          pool:      0x0061B8b1191394FA710Def946368675B79DB062b\n  category:  5\n
          timestamp: 2018-11-26T12:20:40.000Z\n- \n  id:        1394\n  price: 
          15897\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n 
          category:  5\n  timestamp: 2018-11-23T17:13:24.000Z\n- \n  id:  
          1340\n  price:     17024\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n 
          category:  5\n  timestamp: 2018-11-15T14:11:40.000Z\n\nℹ trade in the browser at https://market.iex.ec\n')
"""
        _nborder = 0
        list = intext.split()
        for word in list:
            if word == "id:":
                _nborder += 1

        self.assertEqual(_nborder, 5)

    def test_find_class_order_orderbook(self):
        intext = """('', 'ℹ using chain [kovan]\n- showing orderbook...\n✔ orderbook details:\n- \n  id:        1432\n price:     15270\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp: 2018-11-29T17:28:24.000Z\n- \n  id:        1328\n  price:     15336\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp: 2018-11-13T14:19:44.000Z\n- \n  id:        1401\n  price:     15743\n  pool
        :      0x0061B8b1191394FA710Def946368675B79DB062b\n  category:  5\n  timestamp: 2018-11-26T12:20:40.000Z\n- \n  id:        1394\n  price:     15897\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n            timestamp: 2018-11-23T17:13:24.000Z\n- \n  id:        1340\n  price:     17024\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp: 2018-11-15T14:11:40.000Z\n\nℹ trade in the browser at https://market.iex.ec\n')
"""
        _firstorder = Orderlist(cat=[3, 5])
        _firstorder.fill_ob(intext)
#        for i in _firstorder.book:
#            print(str(i.show()))
        self.assertEqual(_firstorder.book[4].show(),
                         ['1340', '17024', '0x49327538C2f418743E70Ca3495888a62B587A641', '5', '2018-11-15T14:11:40.000Z'])

    def test_create_a_class_order(self):
        intext = """('', 'ℹ using chain [kovan]\n- showing orderbook...\n✔ orderbook details:\n- \n  id:  
        1432\n  price:     15270\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp:
         2018-11-29T17:28:24.000Z\n- \n  id:        1328\n  price:     15336\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp: 2018-11-13T14:19:44.000Z\n- \n  id:        1401\n  price:    
          15743\n  pool:      0x0061B8b1191394FA710Def946368675B79DB062b\n  category:  5\n  timestamp: 2018-11-26T12:20:40.000Z\n- \n  id:        1394\n  price:     15897\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A
          641\n  category:  5\n  timestamp: 2018-11-23T17:13:24.000Z\n- \n  id:        1340\n  price:     17024\n  pool:
                0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  timestamp: 2018-11-15T14:11:40.000Z\n\nℹ
                 trade in the browser at https://market.iex.ec\n')
        """

        _firstorder = Orderlist(cat=[3, 4, 5])
        _firstorder.fill_ob(intext)
#        for i in _firstorder.book:
#            print(str(i.show()))
        self.assertEqual(_firstorder.book[0].show(), ['1432', '15270', '0x49327538C2f418743E70Ca3495888a62B587A641', '5',
                                     '2018-11-29T17:28:24.000Z'])

    def test_find_all_class_orders(self):
        intext = """('', 'ℹ using chain [kovan]\n- showing orderbook...\n✔ orderbook details:\n- \n  
        id:        1432\n  price:     15270\n  pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  
        category:  5\n  timestamp: 2018-11-29T17:28:24.000Z\n- \n  id:        1328\n  price:     15336\n  
        pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  
        timestamp: 2018-11-13T14:19:44.000Z\n- \n  id:        1401\n  price:     15743\n  
        pool:      0x0061B8b1191394FA710Def946368675B79DB062b\n  category:  5\n  
        timestamp: 2018-11-26T12:20:40.000Z\n- \n  id:        1394\n  price:     15897\n  
        pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n 
         timestamp: 2018-11-23T17:13:24.000Z\n- \n  id:        1340\n  price:     17024\n  
         pool:      0x49327538C2f418743E70Ca3495888a62B587A641\n  category:  5\n  
         timestamp: 2018-11-15T14:11:40.000Z\n\nℹ trade in the browser at https://market.iex.ec\n')
        """
        _firstorder = Orderlist(cat=[3, 4, 5])
        _firstorder.fill_ob(intext)
#        for i in _firstorder.book:
#            print(str(i.show()))
        self.assertEqual(_firstorder.book[3].id, "1394")

if __name__ == '__main__':
    unittest.main()
