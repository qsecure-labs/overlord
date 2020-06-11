import cmd2
import os
import argparse
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import random
import string
import json

module = {}
domain_names = []
campaign_list = []
modules_ids = []

class main(list):
    """Main function to initialize variables and calls the cmd2 package for the dns_records module """
    def __init__(self,domains,campaign,mod,project_id):
        global domain_names
        global campaign_list
        global module

        campaign_list = campaign
        domain_names = domains
        if mod is not None:
            module = mod

        # Call cmd_main class 
        i = cmd_main()
        i.prompt = "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( project_id, fg='bright_black', bg='',bold=True, underline=False) + cmd2.ansi.style("/dns_records", fg='blue', bg='',bold=True, underline=False) +")" +"$> "
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
    """cmd2 instance for dns_records module"""

    providers_list = []
    types_list = ["A","MX","TXT"] #["AAAA", "CAA", "CNAME", "MX", "NAPTR", "NS", "PTR", "SOA", "SPF", "SRV"]
    values_list = ["v=DMARC1; p=none; sp=none;","v=spf1 mx -all"]
    # The mod dictionary for the dns_records module    
    mod ={}

    def __init__(self):
        super().__init__()
        #Hide the Quit funcitionality ( if it is deleted it causes erros)
        hide_cmd2_modules(self)

        global campaign_list
        global modules_ids        
        global module
        global domain_names
        
        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 
                self.mod = config["mod_dns_record"]
                self.providers_list = config["providers_list"]
                self.module_provider_parser.choices = self.providers_list
        else:
            print("The config/config.json file does not exists! Exiting...")
            return True  
         
        # Check if the editmodule functionality was used
        if module:
            self.mod = dict(module)
        else:
            self.mod["id"] = randomString()

        # Create list with modules id
        modules_ids = []
        for c in campaign_list:
            if c["module"] != "dns_record" and c["module"] != "letsencrypt" and c["module"] != "godaddy" and  c["module"] != "ansible":
                if c["module"] == "mail" or c["module"] == "redirector":
                    modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
                else:
                    modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
                    for i in range(c["redirectors"]):
                        modules_ids.insert(len(modules_ids),(c["id"]+"-"+str(i+1)+"/"+c["module"]))

        self.domain_recrod_parser.choices = domain_names
        self.module_recrod_parser.choices = modules_ids

    def do_back(self,arg):
        """Return to main menu"""
        return True

    def do_clear(self,arg):
        """Clears screen"""
        os.system('clear')
        
    def do_info(self, mod):
        """Prints variable table or contents of a module added to the campain"""
        if mod:
            x = PrettyTable()
            x.title = mod["module"] + "/"+ mod["id"]
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id",mod["id"] , "N/A", ""])
            x.add_row(["provider", mod["provider"], "yes", "Provider to be used"])
            x.add_row(["type", mod["type"], "yes", "The record type to add. Valid values are A, MX and TXT."])
            x.add_row(["record", mod["records"], "yes", "The record to add.\n  A:   set record -m <module_id> -d <domain>\n  TXT: set record -d <domain> -t <template>/-v <custom>\n  MX:  set record -m <module_id> -d <domain>"])
            x.add_row(["name",mod["name"] , "yes", "Use @ to create the record at the root of the domain or enter a hostname to create it elsewhere.\nA records are for IPv4 addresses only and tell a request where your domain should direct to. For AWS the '@' is converted to ''."])
            x.add_row(["priority",mod["priority"] , "no", "Used for mail server. Default 1."])
            x.add_row(["ttl",mod["ttl"] , "no", "Time to live"])
            x.align["DESCRITPION"] = "l"
        else:            
            x = PrettyTable()
            x.title = 'DNS Records module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id",self.mod["id"] , "N/A", ""])
            x.add_row(["provider", self.mod["provider"], "yes", "Provider to be used"])
            x.add_row(["type", self.mod["type"], "yes", "The record type to add. Valid values are A, MX and TXT."])
            x.add_row(["record", self.mod["records"], "yes", "The  record to add.\n  A:   set record -m <module_id> -d <domain>\n  TXT: set record -d <domain> -t <template>/-v <custom>\n  MX:  set record -m <module_id> -d <domain>"])
            x.add_row(["name",self.mod["name"] , "yes", "Use @ to create the record at the root of the domain or enter a hostname to create it elsewhere.\nA records are for IPv4 addresses only and tell a request where your domain should direct to."])
            x.add_row(["priority",self.mod["priority"] , "no", "Used for mail server. Default 1,"])
            x.add_row(["ttl",self.mod["ttl"] , "no", "Time to live"])
            x.align["DESCRITPION"] = "l"
        print(x)

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='set-command help')


    # create the parser for the "type" sub-command
    parser_type = set_subparsers.add_parser('type', help='The record type to add. Valid values are A, AAAA, CAA, CNAME, MX, NAPTR, NS, PTR, SOA, SPF, SRV and TXT.')
    parser_type.add_argument('type',choices=types_list, type=str, help='example: [ set type <MX> ]')

    # create the parser for the "provider" sub-command
    parser_provider = set_subparsers.add_parser('provider', help='Provider to be used ')
    module_provider_parser = parser_provider.add_argument('provider',choices=providers_list, type=str, help='example: [ set provider <digitalocean> ]')

    # create the parser for the "name" sub-command
    parser_name = set_subparsers.add_parser('name', help='Use @ to create the record at the root of the domain or enter a hostname to create it elsewhere. A records are for IPv4 addresses only and tell a request where your domain should direct to.')
    parser_name.add_argument('name', type=str, help='example: [ set name www ], [ set name @]')

    # create the parser for the "priority" sub-command
    parser_priority = set_subparsers.add_parser('priority', help='Set priority')
    parser_priority.add_argument('priority', type=int, help='example: [ set priority <1> ]')

    # create the parser for the "record" sub-command
    parser_record = set_subparsers.add_parser('record', help="""Sets the record\n            examples\n            A:   set record -m <module_id> -d <domain>\n            TXT: set record -d <domain> -t <template> / set record -d <domain> -v <custom>\n            MX:  set record -m <module_id> -d <domain>""")
    module_recrod_parser = parser_record.add_argument('-m','--module', type=str, help='Module ID to add') #choices=campaign_list,
    # parser_record.add_argument('-r','--redirector', type=int, help='Redirector of module to use')
    domain_recrod_parser =parser_record.add_argument('-d','--domain', type=str, help='domain to use') #,choices=domain_names,
    parser_record.add_argument('-v','--value',type=str, help='Custom vaule to be added') #  ,nargs="?"
    parser_record.add_argument('-t','--txt_templ',type=str,choices = values_list, help='TXT predifined records')

    def set_type(self, arg):
        """Sets the type variable"""
        self.mod["type"]= arg.type
        global campaign_list
        global modules_ids
        modules_ids = []
        if arg.type == "MX":
            for c in campaign_list:
                if c["module"] == "mail" :
                    modules_ids.insert(len(modules_ids),c["id"])
            self.module_recrod_parser.choices = modules_ids
        else:
            for c in campaign_list:
                    if c["module"] != "dns_record" and c["module"] != "letsencrypt" and c["module"] != "redirector" and c["module"] != "godaddy" and  c["module"] != "ansible":
                        if c["module"] == "mail":
                            modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
                        else:
                            modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
                            for i in range(c["redirectors"]):
                                modules_ids.insert(len(modules_ids),(c["id"]+"-"+str(i+1)+"/"+c["module"]))
            self.module_recrod_parser.choices = modules_ids

    def set_name(self, arg):
        """Sets the name variable"""
        if arg.name == "@" and self.mod["provider"] == "aws":
            self.mod["name"] = ""
        elif arg.name == "" and self.mod["provider"] == "digitalocean":
            self.mod["name"] = "@"
        else:
            self.mod["name"] = arg.name

    def set_priority(self, arg):
        """Sets the priority variable"""
        self.mod["priority"]= arg.priority
    
    def set_provider(self, arg):
        """Sets the provider variable"""
        # Check if a provider exists to set up a dns record
        do_flag= False
        aws_flag= False
        global campaign_list

        if arg.provider == "aws":
            for c in campaign_list:
                if c["provider"] == "aws":
                    aws_flag = True
            if not aws_flag:
                print("No aws module was set! Returing without setting the value")
                return
        if arg.provider == "digitalocean":
            for c in campaign_list:
                if c["provider"] == "digitalocean":
                    do_flag = True
            if not do_flag:
                print("No digitalocean module was set! Returing without setting the value")     
                return
        
        self.mod["provider"]= arg.provider
        if self.mod["name"] == "@" and self.mod["provider"] == "aws":
            self.mod["name"] = ""
        elif self.mod["name"] == "" and self.mod["provider"] == "digitalocean":
            self.mod["name"] = "@"
    
    def set_record(self, arg):
        """Sets the record"""
        global campaign_list
        record = {}
        if self.mod["type"] == "MX":
            if  arg.module is not None:
                for c in campaign_list:
                    if c["module"] == "mail" and c["id"] == arg.module.split('/')[0]:
                        record = {c["domain_name"]: c["subdomain"]+"."+c["domain_name"]+"."}
                        self.mod["records"]= record
                if record is None:
                    print("The module is not a mail server")
                
        elif self.mod["type"] == "TXT":
            if arg.txt_templ is not None:
                if arg.domain is not None and arg.value is None:
                    record = {arg.domain: arg.txt_templ}
                    self.mod["records"]= record
                else:
                    print("The txt type requires domain and value or txt_templ to be set")
            else:
                if arg.domain is not None and arg.txt_templ is None:
                    record = {arg.domain: arg.value}
                    self.mod["records"]= record
                else:
                    print("The txt type requires domain and value or txt_temp to be set")
        
        else:
            if arg.domain is not None and arg.module is not None: # and arg.redirector:
                for c in campaign_list:                       
                    if arg.module.split('-')[0] == c["id"]:
                        record = {arg.domain: arg.module.split('/')[0]}
                        self.mod["records"]= record
                        break
                    elif arg.module.split('/')[0] == c["id"]:
                        record = {arg.domain: arg.module.split('/')[0]}
                        self.mod["records"]= record 
            else:
                print("The A type requires domain and a module to be set")

        
    #Set handler functions for the sub-commands
    parser_provider.set_defaults(func=set_provider)
    parser_type.set_defaults(func=set_type)
    parser_name.set_defaults(func=set_name)
    parser_priority.set_defaults(func=set_priority)
    parser_record.set_defaults(func=set_record)

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
        """Adds a dns_record module to the project """
        global  module
        do_flag= False
        aws_flag= False
        global campaign_list

        if not self.mod["records"]:
            print("The variable records can not be None!")      
        elif self.mod["provider"] == "digitalocean":
            for c in campaign_list:
                if c["module"] != "ansible":
                    if c["provider"] == "digitalocean":
                        do_flag = True
                        break
            if not do_flag:
                print("No digitalocean module was set!")
            else:
                module = self.mod
                return True       
        elif self.mod["provider"] == "aws":
            for c in campaign_list:
                if c["module"] != "ansible":
                    if c["provider"] == "aws":
                        aws_flag = True
                        break
            if not aws_flag:
                print("No aws module was set!")
            else:
                module = self.mod
                return True                    
        else:
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
