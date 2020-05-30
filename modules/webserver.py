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
    """Main function to initialize variables and calls the cmd2 package for the webserver module """
    def __init__(self,campaign,mod,project_id):
        global campaign_list
        campaign_list = campaign

        if mod is not None:
            global module
            module = mod

        # Call cmd_main class 
        i = cmd_main()
        i.prompt = "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( project_id, fg='bright_black', bg='',bold=True, underline=False) + cmd2.ansi.style("/webserver", fg='blue', bg='',bold=True, underline=False) +")" +"$> "
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
    """cmd2 instance for webserver module"""
    # The mod dictionary for the webserver module
    mod = {}

    available_regions_list = []
    providers_list = []

    def __init__(self):
        super().__init__()
        global module

        # Hide the Quit funcitionality
        hide_cmd2_modules(self)

        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 
                self.mod = config["mod_webserver"]
                self.providers_list = config["providers_list"]
                self.module_provider_parser.choices = self.providers_list

                for prov in self.providers_list:
                    if self.mod["provider"] == prov:
                        self.available_regions_list = config[prov]["regions"]
                        self.module_regions_parser.choices = self.available_regions_list
                        self.size_list = config[prov]["size"]
                        self.module_size_parser.choices = self.size_list

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
            x.add_row(["provider", mod["provider"], "yes", "Provider to be used "])
            x.add_row(["region",mod["region"] , "yes", "Regions to create Droplet in."])
            x.add_row(["size",mod["size"] , "yes", "Droplet size to launch."])
            x.add_row(["redirectors",mod["redirectors"] , "yes", "Number of redirectors to launch for each webserver."])
            x.align["DESCRITPION"] = "l"
        else:
            x = PrettyTable()
            x.title = 'Webserver module'
            x.field_names = ["VARIABLE", "VALUE", "REQUIRED", "DESCRITPION"]
            x.add_row(["id", self.mod["id"], "N/A", "Module ID"])
            x.add_row(["provider", self.mod["provider"], "yes", "Provider to be used "])
            x.add_row(["region",self.mod["region"] , "yes", "Regions to create Droplet in."])
            x.add_row(["size",self.mod["size"] , "yes", "Droplet size to launch."])
            x.add_row(["redirectors",self.mod["redirectors"] , "yes", "Number of redirectors to launch for each webserver."])
            x.align["DESCRITPION"] = "l"
        print(x)

    # set command
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='Sets the variables of the module')


    # create the parser for the "region" sub-command
    parser_region = set_subparsers.add_parser('region', help='Regions to create Droplet in. Defaults to LON1. Accepted values are NYC1/2/3, SFO1/2, AMS1/2, SGP1, LON1, FRA1, TOR1, BLR1.')
    module_regions_parser = parser_region.add_argument('region',choices=available_regions_list, type=str, help='example : [ set region <AMS1> ]')


    # create the parser for the "redirectors" sub-command
    parser_redirectors = set_subparsers.add_parser('redirectors', help='Number of redirectors to launch for each webserver. Defaults to 1.')
    parser_redirectors.add_argument('redirectors', type=int, help='example: [ set redirectors <3>')

    # create the parser for the "provider" sub-command
    parser_provider = set_subparsers.add_parser('provider', help='Provider to be used ')
    module_provider_parser = parser_provider.add_argument('provider',choices=providers_list, type=str, help='example : [set provider <digitalocean> ]')

    # create the parser for the "size" sub-command
    parser_size = set_subparsers.add_parser('size', help='Size of the droplet.')
    module_size_parser = parser_size.add_argument('size', type=str, help='example: [ set size <s-1vcpu-1gb>] ')

    def set_region(self, arg):
        """Sets the region variable"""
        self.mod["region"]= arg.region
        # Change provider for all modules on AWS
        if self.mod["provider"] == "aws":
            notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
            print(f"""\n{notification} Only one region is supported per project on AWS. {notification}\n""")
            global campaign_list
            for c in campaign_list:
                if c["provider"] == "aws":
                    if c["region"] != arg.region:
                        print(cmd2.ansi.style(f"""Module with {c["id"]} has region set to {c["region"]}. Replacing...""", fg='red', bg='',bold=True, underline=False))
                        c["region"] = arg.region


    def set_redirectors(self, arg):
        """Sets the redirectors variable"""
        self.mod["redirectors"] = arg.redirectors


    def set_provider(self, arg):
        """Sets the provider variable"""
        self.mod["provider"]= arg.provider

        dir_path = "config"
        if  os.path.exists(dir_path+"/config.json"):
            with open(dir_path+'/config.json', 'r') as filehandle:
                config = json.load(filehandle) 

                for prov in self.providers_list:
                    if self.mod["provider"] == prov:
                        self.available_regions_list = config[prov]["regions"]
                        self.module_regions_parser.choices = self.available_regions_list
                        self.size_list = config[prov]["size"]
                        self.module_size_parser.choices = self.size_list
                        self.mod["region"] = config[prov]["default_region"]
                        self.mod["size"] = config[prov]["default_size"]

    def set_size(self, arg):
        """Sets the size variable"""
        self.mod["size"]= arg.size

    #Set handler functions for the sub-commands
    parser_size.set_defaults(func=set_size)
    parser_region.set_defaults(func=set_region)
    parser_redirectors.set_defaults(func=set_redirectors)
    parser_provider.set_defaults(func=set_provider)

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
