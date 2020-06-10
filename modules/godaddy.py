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
domain_list =[]
class main(list):
    """Main function to initialize variables and calls the cmd2 package for the godaddy module """
    def __init__(self,campaign,domains,mod,project_id):
        global campaign_list
        campaign_list = campaign
        global domain_list 
        domain_list = domains
        if mod is not None:
            global module
            module = mod

        # Call cmd_main class 
        i = cmd_main()
        i.prompt = "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( project_id, fg='bright_black', bg='',bold=True, underline=False) + cmd2.ansi.style("/godaddy", fg='blue', bg='',bold=True, underline=False) +")" +"$> "
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
    """cmd2 instance for godaddy module"""
    # The mod dictionary for the godaddy module
    mod = {}

    providers_list = []

    def __init__(self):
        super().__init__()
        global module
        global domain_list
        # Hide the Quit funcitionality
        hide_cmd2_modules(self)

        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 
                self.mod = config["mod_godaddy"]
                self.providers_list = config["providers_list"]
                # self.module_provider_parser.choices = self.providers_list
                self.module_domain_parser.choices = domain_list

        else:
            print("The config/config.json file does not exists! Exiting...")
            return True  
        
        # Check if the editmodule functionality was used
        if module:
            self.mod = dict(module)
        else:
            self.mod["id"] = randomString()
        

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
            x.add_row(["provider", mod["provider"], "N/A", "Autoloaded from domain"])
            x.add_row(["domain", mod["domain"], "yes", "Domain to be used"])
            x.align["DESCRITPION"] = "l"
        else:
            x = PrettyTable()
            x.title = 'Godaddy module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", self.mod["id"], "N/A", "Module ID"])
            x.add_row(["provider", self.mod["provider"], "N/A", "Autoloaded from domain"])
            x.add_row(["domain", self.mod["domain"], "yes", "Domain to be used"])
            x.align["DESCRITPION"] = "l"
        print(x)

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='Sets the variables of the module')

    # create the parser for the "provider" sub-command
    # parser_provider = set_subparsers.add_parser('provider', help='Provider to be used')
    # module_provider_parser = parser_provider.add_argument('provider',choices=providers_list, type=str, help='example : [set provider <digitalocean> ]')

    # create the parser for the "domain" sub-command
    parser_domain = set_subparsers.add_parser('domain', help='Domain to be used')
    module_domain_parser = parser_domain.add_argument('domain',choices=providers_list, type=str, help='example : [set domain <domain> ]')
  
    # def set_provider(self, arg):
    #     """Sets the provider variable"""
    #     self.mod["provider"]= arg.provider

    def set_domain(self, arg):
        """Sets the domain variable"""
        flag = 0
        for mod in campaign_list:
            if mod["module"] == "dns_record":
                if arg.domain == list(mod["records"].keys())[0]:
                    self.mod["domain"]= arg.domain
                    self.mod["provider"]= mod["provider"]
                else:
                    flag = 1
        
        if flag == 1:
            print ("A DNS record must be set for the specified domain before redirecting the NS!")
        
    #Set handler functions for the sub-commands
    # parser_provider.set_defaults(func=set_provider)
    parser_domain.set_defaults(func=set_domain)

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
        if self.mod["domain"]:
            module = self.mod
            return True         
        else:
            print("The domain can not be None!")
    # Command categories
    CMD_CAT_GENERAL = 'General (type help <command>)'
    CMD_CAT_MODULE  = 'Module  (type help <command>)'

    cmd2.categorize((do_add,do_set), CMD_CAT_MODULE)
    cmd2.categorize(do_info, CMD_CAT_GENERAL)
    
def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
