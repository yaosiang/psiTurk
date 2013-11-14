"""
Usage: 
    psiturk_shell
    psiturk_shell setup_example
    psiturk_shell dashboard

"""


from cmd2 import Cmd
import sys
from docopt import docopt, DocoptExit
import re
import readline


from amt_services import MTurkServices
from version import version_number
from psiturk_config import PsiturkConfig
import experiment_server_controller as control


#Escape sequences for display
class color:
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

#################################
#decorator function borrowed from docopt
#################################
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

#################################
# psiturk shell class
#################################
class psiTurk_Shell(Cmd):


    def __init__(self, config, server):
        Cmd.__init__(self)
        self.config = config
        self.server = server
        self.live = 0
        self.sandbox = 0
        self.colorPrompt()
        self.intro = color.GREEN + 'psiTurk version ' + version_number + '\nType "help" for more information.' + color.END

    
    #################################
    # colorPrompt
    #################################
    def colorPrompt(self):
        prompt =  '[' + color.BOLD + 'psiTurk' + color.END
        serverSring = ''
        if self.server.is_server_running():
            serverString = color.GREEN + 'on' + color.END
        else:
            serverString =  color.RED + 'off' + color.END

        prompt += ' exp:' + serverString
        sandboxString =  ''
        if self.sandbox:
            sandboxString = '1'
        else:
            sandboxString = '0'
        prompt += ' #sand:'+sandboxString
        liveString = []
        if self.live:
            liveString = '1'
        else:
            liveString = '0'
        prompt += ' #live:'+liveString
        prompt += ']$ '
        self.prompt =  prompt
    
    #################################
    # postcmd (runs after every command)
    #################################
    def postcmd(self, stop, line):
        self.colorPrompt()
        return Cmd.postcmd(self, stop, line)

    #################################
    # dashboard
    #################################    
    @docopt_cmd
    def do_dashboard(self, arg):
        """
        Usage: dashboard [options]
   
        -i <address>, --ip <address>    IP to run dashboard on. [default: localhost].
        -p <num>, --port <num>          Port to run dashboard on. [default: 22361].
        """

        arg['--port'] = int(arg['--port'])
        import dashboard_server as dbs
        dbs.launch(ip=arg['--ip'], port=arg['--port'])


    #################################
    # version
    #################################

    def do_version(self, arg):
        print 'psiTurk version ' + version_number

    #################################
    # config
    #################################

    def do_print_config(self, arg):

        f = open('config.txt', 'r')
        for line in f:
            sys.stdout.write(line)

    #################################
    # status
    ################################# 

    def do_status(self, arg):
        if self.server.is_server_running():
            print 'Server: ' + color.GREEN + 'currently online' + color.END
        else:
            print 'Server: ' + color.RED + 'currently offline' + color.END
        print 'AMT worker site: ' + str(self.live) + ' HITs available'
        print 'AMT woker sandbox: ' + str(self.sandbox) + ' HITs available'


    #################################
    # create_hit
    #################################

    @docopt_cmd
    def do_create_hit(self, arg):
        """
        Usage: create_hit
               create_hit <where> <numWorkers> <reward> <duration>
        """
        interactive = False
        if arg['<where>'] == None:
            interactive = True
            r = raw_input('[' + color.BOLD + 's' + color.END + ']andbox or [' + color.BOLD + 'l' + color.END + ']ive? ')
            if r=='s':
                arg['<where>'] = 'sandbox'
            elif r=='l':
                arg['<where>'] = 'live'
           
        if arg['<where>']!='sandbox' and arg['<where>']!='live':
            print '*** invalid experiment location'
            return

        if interactive:
            arg['<numWorkers>'] = raw_input('number of participants? ')
            
        try:
            int(arg['<numWorkers>'])
        except ValueError:
            print "*** number of participants must be a whole number"
            return
        if int(arg['<numWorkers>']) <= 0:
            print "*** number of participants must be greater than 0"
            return
        if interactive:
            arg['<reward>'] = raw_input('reward per HIT? ')
        p = re.compile('\d*.\d\d')
        m = p.match(arg['<reward>'])
        if m == None:
            print '*** reward must have format [dollars].[cents]'
            return
        if interactive:
            arg['<duration>'] = raw_input('duration of hit (in minutes)? ')
        try:
            int(arg['<duration>'])
        except ValueError:
            print '*** duration must be a whole number'
            return
        if int(arg['<duration>'])<= 0:
            print '*** duration must be greater than 0'
            return
        total = float(arg['<numWorkers>']) * float(arg['<reward>'])
        fee = total/10
        total = total + fee
        print '*****************************'
        print '  Creating HIT on \'' + arg['<where>'] + '\''
        print '    Max workers: ' + arg['<numWorkers>']
        print '    Reward: $' + arg['<reward>']
        print '    Duration: ' + arg['<duration>'] + ' minutes'
        print '    Fee: $%.2f' % fee
        print '    ________________________'
        print '    Total: $%.2f' % total


    #################################
    # setup_example
    #################################
    def do_setup_example(self, arg):
        import setup_example as se
        se.setup_example()

    #################################
    # launch_server
    #################################
    def do_launch_server(self, arg):
        print self.server.startup()


    #################################
    # shutdown_server
    #################################
    def do_shutdown_server(self, arg):
        self.server.shutdown()

    #################################
    # restart_server
    #################################
    def do_restart_server(self, arg):
        self.server.restart()

    #################################
    # get_workers
    #################################
    def do_get_workers(self, arg):
        services = MTurkServices(self.config)
        print services.get_workers()

    #################################
    # approve_worker
    #################################
    @docopt_cmd
    def do_approve_worker(self, arg):
        """
        Usage: approve_worker (--all | <assignment_id> ...)
        Options:
        --all        approve all completed workers

        """
        services = MTurkServices(self.config)
        if arg["--all"]:
            workers = services.get_workers()
            for worker in workers:
                server.approve_worker(worker["assignmentId"])
        else:
            for assignmentID in arg["<assignment_id>"]:
                server.approve_worker(assignmentID)
    
    #################################
    # reject_worker
    #################################
 #   @docopt_cmd
#    def do_reject_worker(self, arg):

    #################################
    # check_balance
    #################################
    def do_check_balance(self, arg):
        services = MTurkServices(self.config)
        print services.check_balance()
        
        


#################################
# run command loop
#################################
def run():
    opt = docopt(__doc__, sys.argv[1:])
    config = PsiturkConfig()
    config.load_config()
    server = control.ExperimentServerController(config)
    shell =psiTurk_Shell(config, server)
    shell.cmdloop()
