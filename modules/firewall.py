import cmd2
from cmd2.ansi import Fg
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
        i.prompt = "(" + cmd2.ansi.style("Overlord", fg=Fg.RED, bg=None,bold=True, underline=False) + " : " + cmd2.ansi.style( project_id, fg=Fg.DARK_GRAY, bg=None,bold=True, underline=False) + cmd2.ansi.style("/firewall", fg=Fg.BLUE, bg=None,bold=True, underline=False) +")" +"$> "
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
                self.mod = config["mod_firewall"]
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
        modules_ids=[]
        for c in campaign_list:
            if c["module"] != "dns_record" and c["module"] != "letsencrypt" and c["module"] != "godaddy" and c["module"] != "redirector":
                modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
        self.module_mod_id_parser.choices = modules_ids      

        # for c in campaign_list:
        #     if c["module"] != "dns_record" and c["module"] != "letsencrypt" and c["module"] != "godaddy":
        #         if c["module"] == "mail" or c["module"] == "redirector":
        #             modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
        #         else:
        #             modules_ids.insert(len(modules_ids),(c["id"]+"/"+c["module"]))
        #             for i in range(c["redirectors"]):
        #                 modules_ids.insert(len(modules_ids),(c["id"]+"-"+str(i+1)+"/"+c["module"]))
        self.module_mod_id_parser.choices = modules_ids     
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
            x.add_row(["provider", mod["provider"], "yes", "Provider to be used"])
            x.add_row(["protocol", mod["protocol"], "yes", "Protocol for the rule [tcp,udp,icmp]"])
            x.add_row(["port", mod["port"], "yes", "Port or Range of ports [22,0-65535]"])
            x.add_row(["address", mod["address"], "yes", "Addresses for the rule. Default 0.0.0.0/0. It can take more than one seperated by space"])           
            x.add_row(["mod_id", mod["mod_id"], "yes", "Module to be used"])
            x.add_row(["rule", mod["rule"], "yes", "Rule to be used [inbound,outbound]"])                         
            x.align["DESCRITPION"] = "l"
        else:
            x = PrettyTable()
            x.title = 'Firewall module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", self.mod["id"], "N/A", "Module ID"])
            x.add_row(["provider", self.mod["provider"], "yes", "Provider to be used"])
            x.add_row(["protocol", self.mod["protocol"], "yes", "Protocol for the rule [tcp,udp,icmp]"])
            x.add_row(["port", self.mod["port"], "yes", "Port or Range of ports [22,0-65535]"])
            x.add_row(["address", self.mod["address"], "yes", "Addresses for the rule. Default 0.0.0.0/0. It can take more than one seperated by space"])       
            x.add_row(["mod_id", self.mod["mod_id"], "yes", "Module to be used"])
            x.add_row(["rule", self.mod["rule"], "yes", "Rule to be used [inbound,outbound]"])                 
            x.align["DESCRITPION"] = "l"
        print(x)

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='Sets the variables of the module')

    # create the parser for the "provider" sub-command
    parser_provider = set_subparsers.add_parser('provider', help='Provider to be used')
    module_provider_parser = parser_provider.add_argument('provider',choices=providers_list, type=str, help='example : [set provider <digitalocean> ]')
  
    # create the parser for the "port" sub-command
    parser_port = set_subparsers.add_parser('port', help='Ports to be used')
    module_port_parser = parser_port.add_argument('port', type=str, help='example : [set port <22-1000> ,set port 22  ]')
    
    # create the parser for the "protocol" sub-command
    parser_protocol = set_subparsers.add_parser('protocol', help='Protocol to be used')
    module_protocol_parser = parser_protocol.add_argument('protocol',choices=["tcp","udp","icmp"], type=str, help='example : [set protocol tcp ]')
    
    # create the parser for the "address" sub-command
    parser_address = set_subparsers.add_parser('address', help='Address to be used')
    module_address_parser = parser_address.add_argument('address', type=str, help='example : [set address 0.0.0.0/0 ]')

    # create the parser for the "rule" sub-command
    parser_rule = set_subparsers.add_parser('rule', help='Rule to be used')
    module_rule_parser = parser_rule.add_argument('rule',choices=["inbound","outbound"], type=str, help='example : [set rule inbound ]')

    # create the parser for the "mod_id" sub-command
    parser_mod_id = set_subparsers.add_parser('mod_id', help='mod_id to be used')
    module_mod_id_parser = parser_mod_id.add_argument('mod_id', type=str, help='example : [set mod_id tcp ]')
    
    def set_port(self, arg):
        """Sets the port variable"""
        self.mod["port"]= arg.port

    def set_rule(self, arg):
        """Sets the rule variable"""
        self.mod["rule"]= arg.rule

    def set_protocol(self, arg):
        """Sets the protocol variable"""
        self.mod["protocol"]= arg.protocol

    def set_provider(self, arg):
        """Sets the provider variable"""
        self.mod["provider"]= arg.provider

    def set_address(self, arg):
        """Sets the address variable"""
        self.mod["address"]= arg.address

    def set_mod(self, arg):
        """Sets the mod_id variable"""
        self.mod["mod_id"]= arg.mod_id
    #Set handler functions for the sub-commands
    parser_provider.set_defaults(func=set_provider)
    parser_address.set_defaults(func=set_address)
    parser_port.set_defaults(func=set_port)
    parser_protocol.set_defaults(func=set_protocol)
    parser_rule.set_defaults(func=set_rule)
    parser_mod_id.set_defaults(func=set_mod)

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
        if self.mod["mod_id"]:
            module = self.mod
            return True         
        else:
            print("The mod_id can not be None!")
        
        if self.mod["port"] and self.mod["protocol"] !="icmp":
            module = self.mod
            return True         
        else:
            print("The port can not be None!") 

        
    # Command categories
    CMD_CAT_GENERAL = 'General (type help <command>)'
    CMD_CAT_MODULE  = 'Module  (type help <command>)'

    cmd2.categorize((do_add,do_set), CMD_CAT_MODULE)
    cmd2.categorize(do_info, CMD_CAT_GENERAL)
    
def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
