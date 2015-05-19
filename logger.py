class Logger(object):
    """ Log to console and file.
    Color message types.
    Show progress.
    """
    def __init__(self, logfilename=None, verbose=False):
        if logfilename is not None:
            self.logfile = open(logfilename, 'w')
        else:
            self.logfile = None
        self.verbose = verbose
        self.cont = False
        if supports_color():
            self.GREEN = '\33[32m'
            self.YELLOW = '\33[33m'
            self.RED = '\33[31m'
        else:
            self.GREEN = self.YELLOW = self.RED = ''
    def __del__(self):
        if self.logfile is not None:
            self.logfile.close()
    def writeout(self, msg, color=''):
        """ All console ouput should call this function. """
        if color == '':
            sys.stdout.write(msg)
        else:
            sys.stdout.write(color)
            sys.stdout.write(msg)
            sys.stdout.write('\33[m\n')
        if self.logfile is not None:
            self.logfile.write(msg)
    def write(self, msg):
        """ File like interface for pexpect. """
        if self.verbose:
            sys.stdout.write(msg)
        if self.logfile is not None:
            self.logfile.write(msg)
    def flush(self):
        """ File like interface for pexpect. """
        sys.stdout.flush()
    def doing(self, *msgs):
        """ Begin functional section. """
        if self.cont:
            self.writeout('\n')
            self.cont = False
        self.writeout(' '.join(msgs))
        self.writeout('...')
        sys.stdout.flush()
        self.cont = True
    def done(self, msg='OK'):
        """ End functional section. """
        self.writeout(msg, self.GREEN)
        self.cont = False
    def info(self, *msgs):
        """ Output text as it comes. """
        if self.cont:
            self.writeout('\n')
            self.cont = False
        self.writeout(' '.join(msgs))
        self.writeout('\n')
    def progress(self):
        """ Show progress. """
        self.writeout('.')
        sys.stdout.flush()
    def warning(self, *msgs):
        """ Output text in yellow as warning. """
        if self.cont:
            self.writeout('\n')
            self.cont = False
        self.writeout('Warning: ' + ' '.join(msgs), self.YELLOW)
    def error(self, *msgs):
        """ Output text in red as error. """
        if self.cont:
            self.writeout('\n')
            self.cont = False
        self.writeout('Error: ' + ' '.join(msgs), self.RED)

def supports_color():
    """
    Returns True if the running system's terminal supports color,
    and False otherwise.
    """
    plat = sys.platform
    supported_platform = (plat != 'Pocket PC' and
        (plat != 'win32' or 'ANSICON' in os.environ))
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True