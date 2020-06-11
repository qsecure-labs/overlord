import cmd2
import os
import argparse
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import random
import string
import json

module = {}
campaign_list = []

class main(list):
    """Main function to initialize variables and calls the cmd2 package for the godaddy module """
    def __init__(self,campaign,mod,project_id):
        global campaign_list
        campaign_list = campaign

        if mod is not None:
            global module
            module = mod

        # Call cmd_main class 
        i = cmd_main()
        i.prompt = "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( project_id, fg='bright_black', bg='',bold=True, underline=False) + cmd2.ansi.style("/ansible", fg='blue', bg='',bold=True, underline=False) +")" +"$> "
        i.cmdloop()

def hide_cmd2_modules(self):
    # Remove most of the functionalities of the cmd2 package
    self.hidden_commands.append('py')
    self.hidden_commands.append('alias')
    self.hidden_commands.append('macro')
    self.hidden_commands.append('script')
    self.hidden_commands.append('shortcuts')
    self.hidden_commands.append('pyscript')
    self.hidden_commands.append('run_pyscript') 
    self.hidden_commands.append('edit')
    self.hidden_commands.append('run_script')
    self.hidden_commands.append('quit')
    self.hidden_commands.append('load')

class cmd_main(cmd2.Cmd):
    """cmd2 instance for firewall module"""
    # The mod dictionary for the firewall module
    mod = {}

    providers_list = []

    def __init__(self):
        super().__init__()
        global module
        global campaign_list
        # Hide the Quit funcitionality
        hide_cmd2_modules(self)

        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 
                self.mod = config["mod_ansible"]
                # self.providers_list = config["providers_list"]

        else:
            print("The config/config.json file does not exists! Exiting...")
            return True  
        
        # Check if the editmodule functionality was used
        if module:
            self.mod = dict(module)
        else:
            self.mod["id"] = randomString()

        # Create list with modules id
        modules_ids=[]
        for c in campaign_list:
            if c["module"] != "dns_record" and c["module"] != "letsencrypt" and c["module"] != "godaddy":
                modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
                for i in range(c["redirectors"]):
                    modules_ids.insert(len(modules_ids),(c["id"]+"-"+str(i+1)+"/"+c["module"]))

        self.module_hosts_parser.choices = modules_ids      

        self.module_hosts_parser.choices = modules_ids     
    def do_back(self, arg):
        """Return to main menu"""
        return True

    def do_clear(self, arg):
        """Clears screen"""
        os.system('clear')

    def do_info(self,mod):
        """Prints variable table"""
        if mod:
            x = PrettyTable()
            x.title = mod["module"] + "/"+ mod["id"]
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", mod["id"], "N/A", "Module ID"])      
            x.add_row(["hosts", mod["hosts"], "yes", "Module to be used"])
            x.add_row(["playbook", mod["playbook"], "yes", "Playbook to be used"])                  
            x.align["DESCRITPION"] = "l"
        else:
            x = PrettyTable()
            x.title = 'Ansible module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", self.mod["id"], "N/A", "Module ID"])   
            x.add_row(["hosts", self.mod["hosts"], "yes", "Module to be used"])
            x.add_row(["playbook", self.mod["playbook"], "yes", "Playbook to be used"])                 
            x.align["DESCRITPION"] = "l"
        print(x)

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='Sets the variables of the module')

    # create the parser for the "hosts" sub-command
    parser_hosts = set_subparsers.add_parser('hosts', help='hosts to be used')
    module_hosts_parser = parser_hosts.add_argument('hosts',nargs="+", type=str, help='example : [set hosts <id> ]')

    parser_playbook = set_subparsers.add_parser('playbook', help='playbook to be used')
    parser_playbook.add_argument('playbook', type=str, help='example : [set playbook <playbook name> ]')    

    def set_mod(self, arg):
        """Sets the hosts variable"""
        self.mod["hosts"]= arg.hosts

    def set_playbook(self, arg):
        """Sets the =playbook variable"""
        self.mod["playbook"]= arg.playbook    

    #Set handler functions for the sub-commands
    parser_hosts.set_defaults(func=set_mod)
    parser_playbook.set_defaults(func=set_playbook)

    @cmd2.with_argparser(set_parser)
    def do_set(self, args):
        """Set the variables for the module"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever sub-command function was selected
            func(self, args)
        else:
            # No sub-command was provided, so call help
            self.do_help('help')

    def do_add(self,args):
        """Adds c2 module to the project """
        global  module
        module = self.mod
        if self.mod["hosts"]:
            module = self.mod
            return True         
        else:
            print("The hosts can not be None!")
        if self.mod["playbook"]:
            module = self.mod
            return True         
        else:
            print("The playbook can not be None!")

    # Command categories
    CMD_CAT_GENERAL = 'General (type help <command>)'
    CMD_CAT_MODULE  = 'Module  (type help <command>)'

    cmd2.categorize((do_add,do_set), CMD_CAT_MODULE)
    cmd2.categorize(do_info, CMD_CAT_GENERAL)
    
def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
