
import sys
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP

import os.path


class Argparser:
    def __init__(self, _input, check_args=True):
        self.error_found, self.err_msg, self.opts = self.get_checked_args(_input, check_args)
        if self.error_found is True:
            print(self.err_msg)
            exit()

    @staticmethod
    def get_checked_args(_input, check_args):
        _error_found = False
        _err_msg = ""
        _parser = OptionParser(prog='PROG', usage='manage workload with iExec SDK')
#        _parser.add_option('--app', dest='appfile', help='Select the app descrition file')
        _parser.add_option('--nbtasks', dest='nbtasks', type=int, help='Select the number of works')
        _parser.add_option('--pollingtime', dest='pollingtime', type=int, help='Select the polling time in second,'
                                                                               ' default=50s', default=50)
        _parser.add_option('--cat_3', dest='cat_3', help='Select the category 3,4,5 with --cat_3 --cat_4 --cat_5',
                           action="store_true", default=False)
        _parser.add_option('--cat_4', dest='cat_4', help=SUPPRESS_HELP, action="store_true", default=False)
        _parser.add_option('--cat_5', dest='cat_5', help=SUPPRESS_HELP, action="store_true", default=False)

        # Optional arguments
        _group = OptionGroup(_parser, title="Additional options")
        _group.add_option('--simulate', dest='simulate',
                          help='Do not buy the order, just simulate all actions',
                          action="store_true", default=False)
        _group.add_option('--logfile', dest='logfile', help=' Save information in log file', default=False)

        _parser.add_option_group(_group)

        if len(sys.argv) < 2:
            _parser.print_help()
            sys.exit(-1)
        (_options, _args) = _parser.parse_args(_input)
        if check_args:

            def missing_opt_message(_optname):
                return "option --" + _optname + " is required. "

            def invalid_opt_message(_optname, _optval, extra_comment=""):
                return "option --" + _optname + " " + _optval + " is not valid. " + extra_comment

            def invalid_category():
                return "Select a least one category of task"

            # Check arguments validity
            if _options.logfile is None:
                _options.log = False
            else:
                _options.log = True
            if _options.nbtasks is None:
                _error_found = True
                _err_msg += missing_opt_message("nbtasks")
            if _options.nbtasks < 1:
                _error_found = True
                _err_msg += invalid_opt_message("nbtasks", " at least 1 task")
            if _options.cat_3 or _options.cat_4 or _options.cat_5:
                _options.category = []
                if _options.cat_3:
                    _options.category.append(3)
                if _options.cat_4:
                    _options.category.append(4)
                if _options.cat_5:
                    _options.category.append(5)
            else:
                _error_found = True
                _err_msg += invalid_category()

            # check files needed, a best check can be done with file validation content and format.
            file1 = "wallet.json"
            file2 = "iexec.json"
            file3 = "chain.json"
            if not (os.path.exists(file1) and os.path.exists(file2) and os.path.exists(file3)):
                _err_msg += "\nValid wallet.json, iexec.json, chain.json is needed to use iExec "
                _error_found = True

            if _error_found:
                _err_msg += "\n ./iexecbot --help for more details"

        # Remove undefined and void arguments from dictionnary
        tmp = vars(_options)
        res = dict((k, v) for k, v in tmp.items() if (v is not None and v != ''))
        return _error_found, _err_msg, res

    def show_args(self, log, hide_notset=False):
        for i, j in self.opts.items():
            if hide_notset and j is not 'not_set':
                log.add("%20s : %s" % (i, j), showdate=False)

    def get_info(self):
        return self.opts
