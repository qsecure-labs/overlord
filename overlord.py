#!/usr/bin/env python3
import cmd2
import os
import time
import sys
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import random
import string
import shutil
import json
sys.path.insert(0, 'modules')
import letsencrypt
import gophish
import dns_records
import webserver
import c2
import redirector
import mail_server
import argparse
import create
import godaddy
import ansible
#import firewall


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

class Overlord(cmd2.Cmd):
    """Main Menu for Overlord."""
    os.system('clear')
    version = cmd2.ansi.style("v.1.0", fg='red', bg='',
                             bold=True, underline=False)
    print(f"""
                     _               _
  _____   _____ _ __| | ___  _ __ __| |
 / _ \ \ / / _ \ '__| |/ _ \| '__/ _` |
| (_) \ V /  __/ |  | | (_) | | | (_| |
 \___/ \_/ \___|_|  |_|\___/|_|  \__,_|
                                        {version}
    """)
    intro = "Welcome to Overlord!\nType help or ? to list commands\n"
    variables = {
        "dotoken": "",
        "domains" :[],
        "aws_access_key": "",
        "aws_secret_key": "",
        "godaddy_access_key": "",
        "godaddy_secret_key": ""
    }
    campaign = []
    modules_ids =[]
    project_id = ""

    def __init__(self):
        super().__init__()
        hide_cmd2_modules(self)
        #Initialize project ID
        dir_path = "projects"
        uniq = True
        while True:
            rand = randomString()
            for p in next(os.walk(dir_path))[1]:
                if p == rand:
                    uniq = False
            if uniq:
                break

        self.project_id = rand

        self.prompt =  "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( rand, fg='bright_black', bg='',bold=True, underline=False) + ")" +"$> "
        self.loadproject_id.choices = next(os.walk(dir_path))[1]
        self.cloneproject_id.choices = next(os.walk(dir_path))[1]

        if  os.path.exists(dir_path+"/variables.json"):
            with open(dir_path+'/variables.json', 'r') as filehandle:
                self.variables = json.load(filehandle)
                self.domain_parser_id.choices = self.variables["domains"]
    
    def do_clear(self, arg):
        """Clear the screen"""
        os.system('clear')

    def do_exit(self, arg):
        """exit to main menu"""
        flag = input(cmd2.ansi.style("Exit? [y/N]:", fg='red', bg='',bold=True, underline=False))
        if  flag == 'y':
            return True

    def do_version(self, arg):
        """Version"""
        print("version 1.0")

    def do_create(self,arg):
        """Creates terraform project from the campaign"""
        dir_path = "projects/"+self.project_id
        self.do_save(None)
        create.main(self.campaign,self.variables,self.project_id)

    newproject_parser = argparse.ArgumentParser(prog='new')
    newproject_id = newproject_parser.add_argument('id', type=str, nargs="?", help='example: new / new <name> ]')

    @cmd2.with_argparser(newproject_parser)
    def do_new(self,arg):
        """Creates new terraform project."""
        dir_path = "projects"
        if arg.id is None:
            uniq = True
            while True:
                rand = randomString()
                for p in next(os.walk(dir_path))[1]:
                    if p == rand:
                        uniq = False
                if uniq:
                    break
            self.project_id = rand
        else:
            self.project_id = arg.id
        self.campaign = []
        proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        print(f"""\n{notification} New project with ID {proj} has been created.  {notification}\n""")
        self.prompt =  "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( self.project_id, fg='bright_black', bg='',bold=True, underline=False) + ")" +"$> "

    def create_dir(self):
        """Creates the project directory"""
        os.system('mkdir projects/'+self.project_id)
        os.system('mkdir projects/'+self.project_id+'/ssh_keys')
        os.system('mkdir projects/'+self.project_id+'/ssh_configs')
        os.system('mkdir projects/'+self.project_id+'/certificates')

    loadproject_parser = argparse.ArgumentParser(prog='load')
    loadproject_id = loadproject_parser.add_argument('id', type=str, help='example: [ load <ID> ]')

    @cmd2.with_argparser(loadproject_parser)
    def do_load(self,arg):
        """Load a project to overlord"""
        dir_path = "projects/"+arg.id
        if  os.path.exists(dir_path):
            with open(dir_path+'/campaign.json', 'r') as filehandle:
                self.campaign = json.load(filehandle)
            with open(dir_path+'/variables.json', 'r') as filehandle:
                self.variables = json.load(filehandle)
            self.project_id = arg.id
            proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
            notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
            print(f"""\n{notification} The project with ID {proj} has been loaded {notification}\n""")
        self.update_choices(self.campaign)
        self.prompt =  "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( self.project_id, fg='bright_black', bg='',bold=True, underline=False) + ")" +"$> "

    cloneproject_parser = argparse.ArgumentParser(prog='clone')
    cloneproject_id = cloneproject_parser.add_argument('id', type=str, help='example: [ clone <ID> ]')
    cloneproject_parser.add_argument('-n','--name', type=str, help='Name of the new project')

    @cmd2.with_argparser(cloneproject_parser)
    def do_clone(self,arg):
        """Clones a project to a new one"""
        project_to_clone = arg.id
        dir_path = "projects/" + project_to_clone
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        new_path = ""
        new_project_name = ""
        if arg.name is None:
            uniq = True
            while True:
                rand = randomString()
                for p in next(os.walk(dir_path))[1]:
                    if p == rand:
                        uniq = False
                if uniq:
                    break
            new_path = "projects/" + rand
            new_project_name  = rand
        else:
            new_path = "projects/" + arg.name
            new_project_name = arg.name    

        if not os.path.exists(new_path):
            command = 'mkdir ' +new_path
            os.system(command)
            shutil.copy(dir_path+'/campaign.json',new_path+'/campaign.json')
            shutil.copy(dir_path+'/variables.json',new_path+'/variables.json')

            self.loadproject_id.choices = next(os.walk("projects"))[1]
            self.cloneproject_id.choices = next(os.walk("projects"))[1]
        
            print(f"""\n{notification} The project with ID {project_to_clone} has been cloned to {new_project_name}  {notification}\n""")
            
        else:
            print(f"""\n{notification} The project with ID {new_project_name} already exists! {notification}\n""")

    #@cmd2.with_argparser(deleteproject_parser)
    def do_delete(self,arg):
        """Deletes a project"""
        flag = input(cmd2.ansi.style("Are you sure? [y/N]:", fg='red', bg='',bold=True, underline=False))
        if  flag == 'y':
            dir_path = "projects/"+self.project_id+"/.terraform"
            if  os.path.exists(dir_path):
                os.system(f"""cd projects/{self.project_id} && /opt/terraform state rm module.redirect_ns""")
                os.system(f"""cd projects/{self.project_id} && /opt/terraform destroy -auto-approve""")
                os.system(f"""rm projects/{self.project_id}/terraform.tfstate*""")
                shutil.rmtree(f"""projects/{self.project_id}/.terraform""")
            notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
            print(f"""\n{notification} Check if terraform exited without an error before you proceed. {notification}\n""")
            flag1 = input(cmd2.ansi.style("Proceding with deleting project directory. Are you sure? [y/N]:", fg='red', bg='',bold=True, underline=False))
            if flag1 == "y":
                shutil.rmtree("projects/"+self.project_id)
                self.loadproject_id.choices = next(os.walk("projects"))[1]
                self.cloneproject_id.choices = next(os.walk("projects"))[1]
                self.update_choices(self.campaign)
                proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
                notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
                print(f"""\n{notification} The project with ID {proj} has been deleted {notification}\n""")


    def do_save(self,arg):
        """Save a project"""
        dir_path = "projects/"+self.project_id
        if not os.path.exists(dir_path):
            self.create_dir()
        with open(dir_path+'/campaign.json', 'w') as filehandle:
            json.dump(self.campaign, filehandle,indent=4)
        with open(dir_path+'/variables.json', 'w') as filehandle:
            json.dump(self.variables, filehandle,indent=4)
        self.loadproject_id.choices = next(os.walk("projects"))[1]
        self.cloneproject_id.choices = next(os.walk("projects"))[1]
        proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        print(f"""\n{notification} The config files for the project with ID {proj} have been created  {notification}\n""")


    def do_rename(self,arg):
        """Rename a project"""
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        if not arg:
            print(f"""\n{notification} You have to specify a new name for your project! {notification}\n""")
        else:
            proj_old = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
            dir_path = "projects/"+self.project_id
            if os.path.exists(dir_path):
                os.rename("projects/"+self.project_id, "projects/"+arg)
            self.project_id = arg

            self.loadproject_id.choices = next(os.walk("projects"))[1]
            self.cloneproject_id.choices = next(os.walk("projects"))[1]

            proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
            print(f"""\n{notification} The project with ID {proj_old} has been renamed to {proj} {notification}\n""")
            self.prompt =  "(" + cmd2.ansi.style("Overlord", fg='red', bg='',bold=True, underline=False) + " : " + cmd2.ansi.style( self.project_id, fg='bright_black', bg='',bold=True, underline=False) + ")" +"$> "

    def do_deploy(self,arg):
        """Deploy current  project"""
        proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        print(f"""\n{notification} Started deployment of project with ID {proj} {notification}\n""")
        os.system(f"""mkdir -p projects/{self.project_id}/.terraform/plugins/linux_amd64 """)
        os.system(f"""cp redbaron/data/plugins/terraform-provider-godaddy_v1.7.3_x4 projects/{self.project_id}/.terraform/plugins/linux_amd64/terraform-provider-godaddy_v1.7.3_x4""")
        os.system(f"""cd projects/{self.project_id} && /opt/terraform init""")
        os.system(f"""cd projects/{self.project_id} && /opt/terraform plan""")
        os.system(f"""cd projects/{self.project_id} && /opt/terraform apply -auto-approve""")
        print(f"""\n{notification} Terraform has finished with the installation {notification}\n""")

    # USEMODULE COMMAND
    # create the top-level parser for the usemodule command
    usemodule_parser = argparse.ArgumentParser(prog='usemodule')
    usemodule_subparsers = usemodule_parser.add_subparsers(title='usemodule-commands', help='usemodule-command help')

    # create the parser for the sub-command
    parser_dns_records = usemodule_subparsers.add_parser('dns_records', help='Settings to create a dns_record instance')
    parser_gophish = usemodule_subparsers.add_parser('gophish', help='Settings to create a gophish instance')
    parser_mail = usemodule_subparsers.add_parser('mail', help='Settings to create a mail instance')
    parser_webserver = usemodule_subparsers.add_parser('webserver', help='Settings to create a webserver instance')
    parser_c2 = usemodule_subparsers.add_parser('c2', help='Settings to create a c2  instance')
    parser_letsencrypt = usemodule_subparsers.add_parser('letsencrypt', help='Settings to create letsencrypt instance')
    parser_redirector = usemodule_subparsers.add_parser('redirector', help='Settings to create redirector instance')
    parser_godaddy = usemodule_subparsers.add_parser('godaddy', help='Settings to create godaddy NS redirection in a provider of choice')
    parser_ansible = usemodule_subparsers.add_parser('ansible', help='Settings to install asnible playbooks')
    #parser_firewall = usemodule_subparsers.add_parser('firewall', help='firewall help')

    def update_choices(self,camp):
        """Update choices of the argparses for:INFO, DELETE ,EDIT module"""
        self.info_mods_id.choices = updateModulesIdList(camp,"info")
        self.del_mods_id.choices = updateModulesIdList(camp,"del")
        self.edit_mods_id.choices = updateModulesIdList(camp,"edit")

    def usemodule_dns_record(self, arg):
        """Opens the DNS_RECORD module for configuration"""
        if not self.variables["domains"]:
            print("No domains are set! [help set domains]")
        elif len(self.campaign) == 0:
            print("No modules are set! [help usemodule]")
        else:
            dns_records.main(self.variables["domains"],self.campaign,None,self.project_id)
            addModule(dns_records.module,self.campaign)
            self.update_choices(self.campaign)
            dns_records.module={}

    def usemodule_redirector(self, arg):
        """Opens the Redirector module for configuration"""
        redirector.main(None,self.campaign,self.project_id)
        addModule(redirector.module,self.campaign)
        self.update_choices(self.campaign)
        redirector.module={}

    def usemodule_c2(self, arg):
        """Opens the C2 module for configuration"""
        c2.main(self.campaign,None,self.project_id)
        addModule(c2.module,self.campaign)
        self.update_choices(self.campaign)
        c2.module={}

    def usemodule_ansible(self, arg):
        """Opens the C2 module for configuration"""
        ansible.main(self.campaign,None,self.project_id)
        addModule(ansible.module,self.campaign)
        self.update_choices(self.campaign)
        ansible.module={}

    # TODO: Maybe in a future update
    # def usemodule_firewall(self, arg):
    #     """Opens the Firewall module for configuration"""
    #     if len(self.campaign) == 0:
    #          print("No modules are set! [help usemodule]")
    #     firewall.main(self.campaign,None)
    #     addModule(firewall.module,self.campaign)
    #     self.update_choices(self.campaign)
    #     firewall.module={}

    def usemodule_godaddy(self, arg):
        """Opens the Godaddy module for configuration"""
        if  not  self.variables["godaddy_access_key"]:
            print("The access key of  Godaddy is not set! [help set godaddy_access_key]")
        elif not self.variables["godaddy_secret_key"]:
            print("The secret key of  Godaddy is not set! [help set godaddy_secret_key]")
        elif not self.variables["domains"]:
            print("No domains are set! [help set domains]")
        else:
            godaddy.main(self.campaign,self.variables["domains"],None,self.project_id)
            addModule(godaddy.module,self.campaign)
            self.update_choices(self.campaign)
            godaddy.module={}

    def usemodule_mail(self, arg):
        """Opens the mail module for configuration"""
        if not self.variables["domains"]:
            print("No domains are set! [help set domains]")
        else:
            mail_server.main(self.variables["domains"],self.campaign,None,self.project_id)
            addModule(mail_server.module,self.campaign)
            self.update_choices(self.campaign)
            mail_server.module={}

    def usemodule_webserver(self, arg):
        """Opens the webserver module for configuration"""
        webserver.main(self.campaign,None,self.project_id)
        addModule(webserver.module,self.campaign)
        self.update_choices(self.campaign)
        webserver.module={}


    def usemodule_gophish(self, arg):
        """Opens the gophish module for configuration"""
        gophish.main(self.campaign,None,self.project_id)
        addModule(gophish.module,self.campaign)
        self.update_choices(self.campaign)
        gophish.module={}

    def usemodule_letsencrypt(self, arg):
        """Opens the letsencrypt module for configuration"""
        a_records = False
        for c in self.campaign:
            if c["module"] == "dns_record" and c["type"]== "A":
                a_records = True
                break
        if a_records == False:
            print("No A records were set! [help usemodule dns_records]")
        else:
            letsencrypt.main(self.campaign,None,self.project_id) #self.variables["domains"]
            addModule(letsencrypt.module,self.campaign)
            self.update_choices(self.campaign)
            letsencrypt.module={}

    # usemodule handler functions for the sub-commands
    parser_dns_records.set_defaults(func=usemodule_dns_record)
    parser_c2.set_defaults(func=usemodule_c2)
    parser_gophish.set_defaults(func=usemodule_gophish)
    parser_mail.set_defaults(func=usemodule_mail)
    parser_webserver.set_defaults(func=usemodule_webserver)
    parser_letsencrypt.set_defaults(func=usemodule_letsencrypt)
    parser_redirector.set_defaults(func=usemodule_redirector)
    parser_godaddy.set_defaults(func=usemodule_godaddy)
    parser_ansible.set_defaults(func=usemodule_ansible)
    # parser_firewall.set_defaults(func=usemodule_firewall)

    @cmd2.with_argparser(usemodule_parser)
    def do_usemodule(self, args):
        """Usemodule command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever sub-command function was selected
            func(self, args)
        else:
            # No sub-command was provided, so call help
            self.do_help('help')

    # DELETEMODULE COMMAND
    # create the parser for the delmodule command
    delmodule_parser = argparse.ArgumentParser(prog='delmodule')
    del_mods_id = delmodule_parser.add_argument('id', type=str,choices=modules_ids, help='delete module')

    @cmd2.with_argparser(delmodule_parser)
    def do_delmodule(self, arg):
        """Deletes a module"""
        if arg.id == "all":
            self.campaign = []
            notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
            print(f"""\n{notification} All modules have been deleted from the campaign {notification}\n""")
        else:
            for idx,c in enumerate(self.campaign):
                if arg.id == c["id"]:
                    self.campaign.pop(idx)
                    mod = cmd2.ansi.style(c["module"], fg='blue', bg='',bold=True, underline=False)
                    mod_id = cmd2.ansi.style(c["id"], fg='blue', bg='',bold=True, underline=False)
                    notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
                    print(f"""\n{notification} Module {mod} with ID {mod_id} has been deleted from the campaign {notification}\n""")

    # EDITMODULE COMMAND
    # create the parser for the editmodule command
    editmodule_parser = argparse.ArgumentParser(prog='editmodule')
    edit_mods_id = editmodule_parser.add_argument('id', type=str,choices=modules_ids, help='example: [ editmodule <ID> ]')

    @cmd2.with_argparser(editmodule_parser)
    def do_editmodule(self, arg):
        """Edits a module"""
        #Checks the module type and pass it to the correct module for processing
        for idx,c in enumerate(self.campaign):
            if arg.id == c["id"]:
                mod = self.campaign.pop(idx)

                if c["module"] == "c2":
                    c2.main(self.campaign,mod,self.project_id)
                    addModule(c2.module,self.campaign)
                    self.update_choices(self.campaign)
                    c2.module={}
                    break

                if c["module"] == "dns_record":
                    dns_records.main(self.variables["domains"],self.campaign,mod,self.project_id)
                    addModule(dns_records.module,self.campaign)
                    self.update_choices(self.campaign)
                    dns_records.module={}
                    break

                if c["module"] == "redirector":
                    redirector.main(mod,self.campaign,self.project_id)
                    addModule(redirector.module,self.campaign)
                    self.update_choices(self.campaign)
                    redirector.module={}
                    break

                if c["module"] == "gophish":
                    gophish.main(self.campaign,mod,self.project_id)
                    addModule(gophish.module,self.campaign)
                    self.update_choices(self.campaign)
                    gophish.module={}
                    break

                if c["module"] == "letsencrypt":
                    letsencrypt.main(self.campaign,mod,self.project_id) #self.variables["domains"]
                    addModule(letsencrypt.module,self.campaign)
                    self.update_choices(self.campaign)
                    letsencrypt.module={}
                    break

                if c["module"] == "mail":
                    mail_server.main(self.variables["domains"],self.campaign,mod,self.project_id)
                    addModule(mail_server.module,self.campaign)
                    self.update_choices(self.campaign)
                    mail_server.module={}
                    break

                if c["module"] == "webserver":
                    webserver.main(self.campaign,mod,self.project_id)
                    addModule(webserver.module,self.campaign)
                    self.update_choices(self.campaign)
                    webserver.module={}
                    break

                if c["module"] == "godaddy":
                    godaddy.main(self.campaign,self.variables["domains"],mod,self.project_id)
                    addModule(godaddy.module,self.campaign)
                    self.update_choices(self.campaign)
                    godaddy.module={}
                    break

                if c["module"] == "ansible":
                    ansible.main(self.campaign,mod,self.project_id)
                    addModule(ansible.module,self.campaign)
                    self.update_choices(self.campaign)
                    ansible.module={}
                    break

                # if c["module"] == "firewall":
                #     firewall.main(self.campaign,mod)
                #     addModule(firewall.module,self.campaign)
                #     self.update_choices(self.campaign)
                #     firewall.module={}
                #     break

    # SET COMMAND
    # create the top-level parser for the set command
    set_parser = argparse.ArgumentParser(prog='set')
    set_subparsers = set_parser.add_subparsers(title='set-commands', help='set-command help')

    # create the parser for the "counter" sub-command
    parser_dotoken = set_subparsers.add_parser('dotoken', help='Sets the Digital Ocean Token')
    parser_dotoken.add_argument('dotoken' ,type=str, help='example : [ set dotoken <token>]')

    parser_aws_secret_key = set_subparsers.add_parser('aws_secret_key', help='Sets the AWS Secret Key')
    parser_aws_secret_key.add_argument('aws_secret_key' ,type=str, help='example : [ set aws_secret_key <token>]')

    parser_aws_access_key = set_subparsers.add_parser('aws_access_key', help='Sets the AWS Access Key')
    parser_aws_access_key.add_argument('aws_access_key' ,type=str, help='example : [ set aws_access_key <token>]')

    parser_godaddy_access_key = set_subparsers.add_parser('godaddy_access_key', help='Sets the Godaddy Access Key')
    parser_godaddy_access_key.add_argument('godaddy_access_key' ,type=str, help='example : [ set godaddy_access_key <token>]')

    parser_godaddy_secret_key = set_subparsers.add_parser('godaddy_secret_key', help='Sets the Godaddy Secret Key')
    parser_godaddy_secret_key.add_argument('godaddy_secret_key' ,type=str, help='example : [ set godaddy_secret_key <token>]')

    parser_domains = set_subparsers.add_parser('domains', help='Domain names to be used in the campaign (Multilpe domain names can be added)')
    parser_domains.add_argument('-a','--add',type=str, help='Domain to be added')
    domain_parser_id = parser_domains.add_argument('-d','--delete',type=str,choices = ("kokos.com","a.com"), help='Domain to be deleted')

    parser_variables = set_subparsers.add_parser('variables', help='Sets the default variables.json to the values that are in memory')
    parser_variables.add_argument('variables',nargs="?", type=str, help='example : [ set variables]')

    def set_dotoken(self, arg):
        """Sets the dotoken"""
        self.variables["dotoken"]= arg.dotoken

    def set_aws_access_key(self, arg):
        """Sets the aws_access_key"""
        self.variables["aws_access_key"]= arg.aws_access_key

    def set_aws_secret_key(self, arg):
        """Sets the aws_secret_key"""
        self.variables["aws_secret_key"]= arg.aws_secret_key

    def set_godaddy_access_key(self, arg):
        """Sets the aws_access_key"""
        self.variables["godaddy_access_key"]= arg.godaddy_access_key

    def set_godaddy_secret_key(self, arg):
        """Sets the aws_access_key"""
        self.variables["godaddy_secret_key"]= arg.godaddy_secret_key

    def set_domains(self, arg):
        """Sets the domains"""
        if arg.add:
            self.variables["domains"].insert((len(self.variables["domains"])),arg.add)
        elif arg.delete:
            for idx,c in enumerate(self.variables["domains"]):
                if arg.delete == c:
                    self.variables["domains"].pop(idx)
        self.domain_parser_id.choices = self.variables["domains"]

    def set_variables(self, arg):
        with open('projects/variables.json', 'w') as filehandle:
                json.dump(self.variables, filehandle,indent=4)

        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        print(f"""\n{notification} Variables have been saved to ./projects/variables.json {notification}\n""")

    #Set handler functions for the sub-commands
    parser_variables.set_defaults(func=set_variables)
    parser_dotoken.set_defaults(func=set_dotoken)
    parser_aws_access_key.set_defaults(func=set_aws_access_key)
    parser_aws_secret_key.set_defaults(func=set_aws_secret_key)
    parser_godaddy_access_key.set_defaults(func=set_godaddy_access_key)
    parser_godaddy_secret_key.set_defaults(func=set_godaddy_secret_key)
    parser_domains.set_defaults(func=set_domains)


    @cmd2.with_argparser(set_parser)
    def do_set(self, args):
        """General variables for the campaign to be set"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever sub-command function was selected
            func(self, args)
        else:
            # No sub-command was provided, so call help
            self.do_help('help')

    # INFO COMMAND
    # create the top-level parser for the info command
    info_parser = argparse.ArgumentParser(prog='info')
    info_mods_id = info_parser.add_argument('id',nargs="?", type=str,choices=modules_ids, help='example: [ info <ID> ]')

    def info_table(self,c):
        """Uses Pretty Table to print the info for a specific campaign object"""
        if c["module"] == "c2":
            c2.cmd_main.do_info(None,c)
        if c["module"] == "redirector":
            redirector.cmd_main.do_info(None,c)
        if c["module"] == "dns_record":
            dns_records.cmd_main.do_info(None,c)
        if c["module"] == "gophish":
            gophish.cmd_main.do_info(None,c)
        if c["module"] == "letsencrypt":
            letsencrypt.cmd_main.do_info(None,c)
        if c["module"] == "mail":
            mail_server.cmd_main.do_info(None,c)
        if c["module"] == "webserver":
            webserver.cmd_main.do_info(None,c)
        if c["module"] == "godaddy":
            godaddy.cmd_main.do_info(None,c)
        if c["module"] == "ansible":
            ansible.cmd_main.do_info(None,c)
        # if c["module"] == "firewall":
        #     firewall.cmd_main.do_info(None,c)

    @cmd2.with_argparser(info_parser)
    def do_info(self, arg):
        """Prints variable table or contents of a module which was added to the campaign"""
        if arg.id is not None:
            #Prints table for all or one module by specifing the ID
            if arg.id == "all":
                for c in self.campaign:
                    self.info_table(c)
            else:
                for c in self.campaign:
                    if arg.id == c["id"]:
                        self.info_table(c)

        else:
            #Prints the general variables and the table with the module IDs
            print(f"Project ID: {self.project_id}")
            if 'dotoken' in self.variables.keys():
                print(f"Digital Ocean Key: {self.variables['dotoken']}")
            if 'aws_access_key' in self.variables.keys():
                print(f"AWS Access Key: {self.variables['aws_access_key']}")
            if 'aws_secret_key' in self.variables.keys():
                print(f"AWS Secret Key: {self.variables['aws_secret_key']}")
            if 'godaddy_access_key' in self.variables.keys():
                print(f"Godaddy Access Key: {self.variables['godaddy_access_key']}")
            if 'godaddy_secret_key' in self.variables.keys():
                print(f"Godaddy Secret Key: {self.variables['godaddy_secret_key']}")
            print(f"Domains: {', '.join(self.variables['domains'])}")
            x = PrettyTable()
            x.title = 'Campaign'
            x.field_names = ["#","MODULE", "ID"]
            for idx,i in enumerate(self.campaign):
                if 'type' in i:
                    x.add_row([idx+1,i["module"] + "/"+ i["type"] , i["id"]])
                else:
                    x.add_row([idx+1,i["module"], i["id"]])
                x.align["DESCRITPION"] = "l"
            print(x)


    # Command categories
    CMD_CAT_GENERAL = 'General (type help <command>)'
    CMD_CAT_MODULE  = 'Module  (type help <command>)'
    CMD_CAT_PROJECT = 'Project (type help <command>)'
    #Help Menu
    cmd2.categorize((do_create,do_new,do_save,do_deploy,do_delete,do_load,do_rename, do_clone), CMD_CAT_PROJECT)
    cmd2.categorize((do_usemodule,do_editmodule,do_delmodule), CMD_CAT_MODULE)
    cmd2.categorize((do_set,do_info), CMD_CAT_GENERAL)

def addModule(module,campaign):
    """Adds a module to the campaign"""
    if module:
        campaign.insert(len(campaign),dict(module))
        mod = cmd2.ansi.style(module["module"], fg='blue', bg='',bold=True, underline=False)
        mod_id = cmd2.ansi.style(module["id"], fg='blue', bg='',bold=True, underline=False)
        notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
        print(f"""\n{notification} Module {mod} with ID {mod_id} has been added to the campaign {notification}\n""")

def updateModulesIdList(campaign,m):
    """Updates the Modules ID list (main use is the argparse choices)"""
    modules_ids = []
    for c in campaign:
        modules_ids.insert(len(modules_ids),c["id"])
    if len(modules_ids) > 0 and m != "edit":
        modules_ids.insert(len(modules_ids),"all")

    return modules_ids

def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == '__main__':
    app = Overlord()
    app.set_window_title("Overlord")
    app.cmdloop()
