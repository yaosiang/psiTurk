"""
Usage: 
    psiturk_shell
    psiturk_shell setup_example
    psiturk_shell dashboard

"""
import sys
import re


from cmd2 import Cmd
from docopt import docopt, DocoptExit
import readline

from amt_services import MTurkServices
from version import version_number
from psiturk_config import PsiturkConfig
import experiment_server_controller as control
import dashboard_server as dbs

#Escape sequences for display

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# decorator function borrowed from docopt
def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return
        return func(self, opt)
    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn



class Psiturk_Shell(Cmd):


    def __init__(self, config, services, server):
        Cmd.__init__(self)
        self.config = config
        self.server = server
        self.services = services
        self.color_prompt()
        self.intro = Color.GREEN + 'psiTurk version ' + version_number + \
                     '\nType "help" for more information.' + Color.END

    def color_prompt(self):
        prompt =  '[' + Color.BOLD + 'psiTurk' + Color.END
        serverSring = ''
        server_status = self.server.is_server_running()
        if server_status == 'yes':
            serverString = Color.GREEN + 'on' + Color.END
        elif server_status == 'no':
            serverString =  Color.RED + 'off' + Color.END
        elif server_status == 'maybe':
            serverString = Color.YELLOW + 'wait' + Color.END
        prompt += ' server:' + serverString  
        usingSandbox = self.config.getboolean('HIT Configuration', 'using_sandbox')
        activeString = ''
        if usingSandbox:
            activeString = ' #sandboxHITs:'
        else:
            activeString = ' #liveHITs:'        
        hits = self.services.get_active_hits()
        if hits:
            numHits = len(hits)
            prompt += activeString + str(numHits)
        else:
            prompt += ' #HITs:0'
        prompt += ']$ '
        self.prompt =  prompt
    
    def postcmd(self, stop, line):
        self.color_prompt()
        return Cmd.postcmd(self, stop, line)

    @docopt_cmd
    def do_dashboard(self, arg):
        """
        Usage: dashboard [options]
   
        -i <address>, --ip <address>    IP to run dashboard on. [default: localhost].
        -p <num>, --port <num>          Port to run dashboard on. [default: 22361].
        """
        arg['--port'] = int(arg['--port'])
        dbs.launch(ip=arg['--ip'], port=arg['--port'])

    def do_version(self, arg):
        print 'psiTurk version ' + version_number

    def do_print_config(self, arg):

        f = open('config.txt', 'r')
        for line in f:
            sys.stdout.write(line)

    def do_status(self, arg):
        server_status = self.server.is_server_running()
        if server_status == 'yes':
            print 'Server: ' + Color.GREEN + 'currently online' + Color.END
        elif server_status == 'no':
            print 'Server: ' + Color.RED + 'currently offline' + Color.END
        elif server_status == 'maybe':
            print 'Server: ' + Color.YELLOW + 'please wait' + Color.END
        print 'AMT worker site: ' + str(self.live) + ' HITs available'
        print 'AMT woker sandbox: ' + str(self.sandbox) + ' HITs available'

    @docopt_cmd
    def do_create_hit(self, arg):
        """
        Usage: create_hit
               create_hit <where> <numWorkers> <reward> <duration>
        """
        interactive = False
        if arg['<where>'] is None:
            interactive = True
            r = raw_input('[' + Color.BOLD + 's' + Color.END +
                          ']andbox or [' + Color.BOLD + 'l' + 
                          Color.END + ']ive? ')
            if r == 's':
                arg['<where>'] = 'sandbox'
            elif r == 'l':
                arg['<where>'] = 'live'
        if arg['<where>'] != 'sandbox' and arg['<where>'] != 'live':
            print '*** invalid experiment location'
            return
        if interactive:
            arg['<numWorkers>'] = raw_input('number of participants? ')
        try:
            int(arg['<numWorkers>'])
        except ValueError:

            print '*** number of participants must be a whole number'
            return
        if int(arg['<numWorkers>']) <= 0:
            print '*** number of participants must be greater than 0'
            return
        if interactive:
            arg['<reward>'] = raw_input('reward per HIT? ')
        p = re.compile('\d*.\d\d')
        m = p.match(arg['<reward>'])

        if m is None:
            print '*** reward must have format [dollars].[cents]'
            return
        if interactive:
            arg['<duration>'] = raw_input('duration of hit (in hours)? ')
        try:
            int(arg['<duration>'])
        except ValueError:
            print '*** duration must be a whole number'
            return
        if int(arg['<duration>']) <= 0:
            print '*** duration must be greater than 0'
            return
        self.config.set('HIT Configuration', 'max_assignments',
                        arg['<numWorkers>'])
        self.config.set('HIT Configuration', 'reward', arg['<reward>'])
        self.config.set('HIT Configuration', 'duration', arg['<duration>'])
        self.services.create_hit()
        #print results
        total = float(arg['<numWorkers>']) * float(arg['<reward>'])
        fee = total / 10
        total = total + fee
        print '*****************************'
        print '  Creating HIT on \'' + arg['<where>'] + '\''
        print '    Max workers: ' + arg['<numWorkers>']
        print '    Reward: $' + arg['<reward>']
        print '    Duration: ' + arg['<duration>'] + ' hours'
        print '    Fee: $%.2f' % fee
        print '    ________________________'
        print '    Total: $%.2f' % total

    def do_setup_example(self, arg):
        import setup_example as se
        se.setup_example()

    def do_launch_server(self, arg):
        self.server.startup()

    def do_shutdown_server(self, arg):
        self.server.shutdown()

    def do_restart_server(self, arg):
        self.server.restart()

    def do_get_workers(self, arg):
        workers = self.services.get_workers()
        if not workers:
            print Color.RED + 'failed to get workers' + Color.END
        else:
            print self.services.get_workers()

    @docopt_cmd
    def do_approve_worker(self, arg):
        """
        Usage: approve_worker (--all | <assignment_id> ...)
        Options:
        --all        approve all completed workers

        """
        if arg['--all']:
            workers = self.services.get_workers()
            for worker in workers:
                success = self.services.approve_worker(worker['assignmentId'])
                if success:
                    print 'approved ' + arg['<assignment_id>']
                else:
                    print '*** failed to approve ' + arg['<assignment_id>']
        else:
            for assignmentID in arg['<assignment_id>']:
                success = self.services.approve_worker(assignmentID)
                if success:
                    print 'approved ' + arg['<assignment_id>']
                else:
                    print '*** failed to approve ' + arg['<assignment_id>']

    
    @docopt_cmd
    def do_reject_worker(self, arg):
        """
        Usage: reject_worker <assignment_id> ...
        """
        for assignmentID in arg['<assignment_id>']:
            success = self.services.reject_worker(assignmentID)
            if success:
                print 'rejected ' + arg['<assignment_id>']
            else:
                print  '*** failed to reject ' + arg['<assignment_id>']


    def do_check_balance(self, arg):
        print self.services.check_balance()
        

    def do_get_active_hits(self, arg):
        hits_data = self.services.get_active_hits()
        if not hits_data:
            print '*** failed to retrieve active hits'
        else:
            print hits_data

    @docopt_cmd
    def do_extend_hit(self, arg):
        """
        Usage: extend_hit <HITid> [options]
        
        -a <number>, --assignments <number>    Increase number of assignments on HIT
        -e <time>, --expiration <time>         Increase expiration time on HIT (hours)
        """
        self.services.extend_hit(self, arg['<HITid>'], arg['--assignments'], 
                            arg['--expiration'])

    @docopt_cmd
    def do_expire_hit(self, arg):
        """
        Usage: expire_hit <HITid>
        """
        self.services.expire_hit(arg['<HITid>'])

def run():
    opt = docopt(__doc__, sys.argv[1:])
    config = PsiturkConfig()
    config.load_config()
    services = MTurkServices(config)
    server = control.ExperimentServerController(config)
    shell = Psiturk_Shell(config, services, server)
    shell.cmdloop()
