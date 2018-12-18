
import sys
from optparse import OptionParser, OptionGroup
from pathlib import Path


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
        _parser.add_option('--cat_3', dest='cat_3', help='Select the category 3', action="store_true", default=False)
        _parser.add_option('--cat_4', dest='cat_4', help='Select the category 4', action="store_true", default=False)
        _parser.add_option('--cat_5', dest='cat_5', help='Select the category 5', action="store_true", default=False)

        # Optional arguments
        _group = OptionGroup(_parser, title="Additional options")
        _group.add_option('--simulate', dest='simulate',
                          help='Do not buy the order, just simulate all actions',
                          action="store_true", default=False)

        if len(sys.argv) < 2:
            _parser.print_help()
            sys.exit(-1)
        (_options, _args) = _parser.parse_args(_input)
        if check_args:

            def missing_opt_message(_optname):
                return "option --" + _optname + " is required. "

            def invalid_opt_message(_optname, _optval, extra_comment=""):
                return "option --" + _optname + " " + _optval + " is not valid. " + extra_comment

            # Check arguments validity
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
                _options.category= [5]

            # check files needed, a best check can be done with file validation content and format.
            file1 = Path("wallet.json")
            file2 = Path("iexec.json")
            file3 = Path("chain.json")
            if not (file1.is_file() and file2.is_file() and file3.is_file()):
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
