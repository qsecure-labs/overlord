import cmd2
import os
import argparse
import sys
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import random
import string
import json

module = {}
domain_names = []
campaign_list = []

class main(list):
    """Main function to initialize variables and calls the cmd2 package for the letsencrypt module """
    def __init__(self,campaign,mod): #domains
        global campaign_list
        global module

        campaign_list = campaign
        if mod is not None:
            module = mod


        # Call cmd_main class 
        i = cmd_main()
        i.prompt = cmd2.ansi.style("Overlord", fg='red', bg='', bold=True, underline=False) + \
            cmd2.ansi.style("/letsencrypt", fg='blue', bg='',
                            bold=True, underline=False) + "$> "
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
    """cmd2 instance for letsencrypt module"""
    # The mod dictionary for the letsencrypt module
    mod = {}

    domain_names = []
    record_list = []

    def __init__(self):
        super().__init__()
        hide_cmd2_modules(self)
        global campaign_list   
        global module
        
        
        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 
                self.mod = config["mod_letsencrypt"]
        else:
            print("The config/config.json file does not exists! Exiting...")
            return True 
 
        # Check if the editmodule functionality was used
        if module:
            self.mod = dict(module)
        else:
            self.mod["id"] = randomString()
        
        # TODO add functionality for wirldcard certificates:
        # https://medium.com/@saurabh6790/generate-wildcard-ssl-certificate-using-lets-encrypt-certbot-273e432794d7

        self.domain_list = []
        self.record_list = []
        for c in campaign_list:
            if c["module"] == "dns_record" and c["type"]== "A":
                if c["name"] == "@" or c["name"] == "":
                    self.record_list.append(c["records"])
                    for k in c["records"].keys():
                        self.domain_list.append(k)
                else:
                    rec =dict(c["records"])
                    for k in c["records"].keys():
                        self.domain_list.append( c["name"]+"."+k)
                    rec[ c["name"]+"."+k] = rec.pop(k)
                    self.record_list.append(rec)

        self.domain_names = self.domain_list
        self.domain_name_parser.choices = self.domain_list

    def do_info(self,mod):
        """Prints variable table"""
        if mod:
            x = PrettyTable()
            x.title = mod["module"] + "/"+  mod["id"]
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", mod["id"], "N/A", "Module ID"])
            x.add_row(["domain_name", mod["domain_name"], "yes", "The domain name for the certificate"])
            x.add_row(["email",mod["email"] , "yes", "Email for certificate defaults to kokos@example.com"])
            x.add_row(["mod_id",mod["mod_id"] , "no", "Autoloaded from domain_name"])
            x.align["DESCRITPION"] = "l"
        else:
            x = PrettyTable()
            x.title = 'Lets Encrypt Module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", self.mod["id"], "N/A", "Module ID"])
            x.add_row(["domain_name", self.mod["domain_name"], "yes", "The domain name for the certificate"])
            x.add_row(["email",self.mod["email"] , "yes", "Email for certificate defaults to kokos@example.com"])
            x.add_row(["mod_id",self.mod["mod_id"] , "no", "Autoloaded from domain_name"])
            x.align["DESCRITPION"] = "l"
        print(x)
    
    def do_back(self,arg):
        """Return to main menu"""
        return True

    def do_clear(self,arg):
        """Clears screen"""
        os.system('clear')

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='set-command help') 

    # create the parser for the "email" sub-command
    parser_email = set_subparsers.add_parser('email', help='Email for certificate defaults to kokos@example.com')
    parser_email.add_argument('email', type=str, help='example: [ set email kokos@example.com ]')

    # create the parser for the "domain name" sub-command
    parser_domain_name = set_subparsers.add_parser('domain_name', help='The domain name for the certificate')
    domain_name_parser = parser_domain_name.add_argument('domain_name',choices=domain_names, type=str, help='example: [ set domain_name <example.com> ]')


    def set_domain_name(self, arg):
        """Sets the domain_name variable"""
        self.mod["domain_name"] = arg.domain_name
        # for idx,item in enumerate(list):
        for idx,d in enumerate(self.domain_names):
            if d ==  arg.domain_name:
                self.mod["mod_id"] = self.record_list[idx][d]
   
    def set_email(self, arg):
        """Sets the email variable"""
        self.mod["email"]= arg.email
    
    #Set handler functions for the sub-commands
    parser_domain_name.set_defaults(func=set_domain_name)
    parser_email.set_defaults(func=set_email)

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
        """Adds letsencrypt module to the project """
        if not self.mod["domain_name"]:
            print("Variable domain_name can not be None")
        elif not self.mod["mod_id"]:
            print("Variable mod_id can not be None")
        else:
            global  module
            module = self.mod
            return True

    # Command categories
    CMD_CAT_GENERAL = 'General (type help <command>)'
    CMD_CAT_MODULE  = 'Module  (type help <command>)'

    cmd2.categorize((do_add,do_set), CMD_CAT_MODULE)
    cmd2.categorize(do_info, CMD_CAT_GENERAL)
    
def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
