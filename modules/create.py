import cmd2
import sys
import os
sys.path.insert(0, 'modules/providers')
import digitalocean
import aws
import secrets
import string

class main(list):
    txt_recs = False
    campaign = []
    project_id = ""
    do_domains = []
    aws_domains = []
    variables = {
        "dotoken": "",
        "domains" :[],
        "aws_access_key": "",
        "aws_secret_key": "",
        "godaddy_access_key": "",
        "godaddy_secret_key": ""
    }

    def __init__(self,camp,variables,pid):

        self.campaign = camp
        self.project_id  = pid
        self.variables = dict(variables)
        self.categorize_domains()

        self.creation()

    def creation(self):
        f= open("projects/"+self.project_id+"/terraform.tf","w+")
        q= open("projects/"+self.project_id+"/variables.tf","w+")

        f.write(self.create_general())
        f.write(self.create_dns_names())

        aws_exception = False
        # Check if AWS is used
        for c in self.campaign:
            if c["module"] != "letsencrypt" and c["module"] != "godaddy" and c["module"] != "ansible":
                if c["provider"] == "aws":
                    try:
                        self.variables["aws_region"] = c["region"]
                        f.write(self.create_aws_vpc())
                        break
                    except:
                        print ("At least one AWS module should be used in the dependent modules!")
                        aws_exception = True
                        break
        
        if not aws_exception:
            for c in self.campaign:
                if c["module"] == "c2":
                    f.write(self.create_c2(c))
                if c["module"] == "redirector":
                    f.write(self.create_redirector(c))
                if c["module"] == "webserver":
                    f.write(self.create_webserver(c))
                if c["module"] == "gophish":
                    f.write(self.create_gophish(c))
                if c["module"] == "mail":
                    if not os.path.exists(f"""projects/{self.project_id}/{c["id"]}/"""):
                        alphabet = string.ascii_letters + string.digits
                        password = ''.join(secrets.choice(alphabet) for i in range(20))
                        os.system(f"""mkdir -p projects/{self.project_id}/{c["id"]}/""")
                        os.system(f"""touch projects/{self.project_id}/{c["id"]}/iredmailpass.txt""")
                        os.system(f"""cd projects/{self.project_id}/{c["id"]}/ && echo {password} > iredmailpass.txt""")
                        os.system(f"""cp redbaron/data/scripts/iredmail.sh projects/{self.project_id}/{c["id"]}/iredmail.sh""")
                        os.system(f"""sed -i 's/domain-to-change.com/{c["domain_name"]}/g' projects/{self.project_id}/{c["id"]}/iredmail.sh""")
                        os.system(f"""sed -i 's/changeme!/{password}/g' projects/{self.project_id}/{c["id"]}/iredmail.sh""")
                    f.write(self.create_mail(c))
                if c["module"] == "dns_record":
                    f.write(self.create_dns_records_type(c))
                if c["module"] == "letsencrypt":
                    f.write(self.create_cert(c))
                if c["module"] == "godaddy":
                    f.write(self.redirect_ns(c))
                if c["module"] == "ansible":
                    f.write(self.create_ansible(c))
                # if c["module"] == "firewall":
                #     f.write(self.create_firewall(c))
            f.close

            #Create the variables.tf file:
            q.write(self.create_variables())

            proj = cmd2.ansi.style(self.project_id, fg='blue', bg='',bold=True, underline=False)
            notification = cmd2.ansi.style("***", fg='red', bg='',bold=True, underline=False)
            print(f"""\n{notification} The terrafrom files for the project with ID {proj} have been created {notification}\n""")


    def categorize_domains(self):
        self.do_domains  =[]
        self.aws_domains =[]

        for camp in self.campaign:
            if camp["module"] == "dns_record":
                if camp["provider"] == "digitalocean":
                    for k in camp["records"].keys():
                        self.do_domains.append(k)
                elif camp["provider"] == "aws":
                        for k in camp["records"].keys():
                            self.aws_domains.append(k)


        self.do_domains = list(set(self.do_domains))
        self.aws_domains = list(set(self.aws_domains))

    def create_aws_vpc(self):
        output = """
// Create VPC for AWS instances
module "create_vpc" {
  source = "../../redbaron/modules/aws/create-vpc"
}"""
        return output

    def create_variables(self):
        domain_string = ', '.join('"{0}"'.format(d) for d in  self.variables["domains"])
        domain_string_aws = ', '.join('"{0}"'.format(d) for d in  self.aws_domains)
        domain_string_do = ', '.join('"{0}"'.format(d) for d in  self.do_domains)
        output=f"""
variable "domain" {{
type    = list
default = [{domain_string}]
}}\n"""
        if len(self.aws_domains ) != 0:
            output= output + f"""
variable "aws_domain" {{
type    = list
default = [{domain_string_aws}]
}}\n"""
        if len(self.do_domains ) != 0:
            output= output + f"""
variable "do_domain" {{
type    = list
default = [{domain_string_do}]
}}\n"""
        # Check if digitalocean is used.
        for c in self.campaign:
            if c["module"] != "letsencrypt" and c["module"] != "ansible":
                if c["provider"] == "digitalocean":
                    output = output +f"""
variable "do_token" {{
default = "{self.variables["dotoken"]}"
}}\n"""
                    break
        # Check if aws is used.
        for c in self.campaign:
            if c["module"] != "letsencrypt" and c["module"] != "ansible":
                if c["provider"] == "aws":
                    output = output +f"""
variable "aws_key" {{
 default = "{self.variables["aws_access_key"]}"
}}

variable "aws_secret" {{
 default = "{self.variables["aws_secret_key"]}"
}}

variable "aws_region" {{
 default = "{self.variables["aws_region"]}"
}}

"""
                    break
        for c in self.campaign:
            if c["module"] == "godaddy":
                output = output +f"""
variable "godaddy_key" {{
 default = "{self.variables["godaddy_access_key"]}"
}}

variable "godaddy_secret" {{
 default = "{self.variables["godaddy_secret_key"]}"
}}
"""
                break
        return output

    def create_general(self):
        output ="""
###################################################################################################################
#                                                Providers                                                        #
###################################################################################################################
"""
        # Check if digitalocean is used.
        for c in self.campaign:
            if c["module"] != "letsencrypt" and c["module"] != "ansible":
                if c["provider"] == "digitalocean":
                    output = output +"""
provider "digitalocean" {
    token = var.do_token
}"""
                    break

        # Check if aws is used.
        for c in self.campaign:
            if c["module"] != "letsencrypt" and c["module"] != "ansible":
                if c["provider"] == "aws":
                    output = output +"""
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_key
  secret_key = var.aws_secret
}
"""
                    break
        for c in self.campaign:
            if c["module"] == "godaddy":
                output = output +"""
provider "godaddy" {
  key =  var.godaddy_key
  secret = var.godaddy_secret
}
"""
                break
        return output


    def redirect_ns(self,c):
        if c["provider"] == "digitalocean":
            output = f"""
module "redirect_ns_{c["id"]}"{{
  source = "../../redbaron/modules/godaddy/redirect-nameservers"
  domain = "{c["domain"]}"
  nameservers = ["ns1.digitalocean.com" , "ns2.digitalocean.com", "ns3.digitalocean.com"]
}}
"""
        elif c["provider"] == "aws":
            public_zone = 0
            for idx,d in enumerate(self.aws_domains):
                if d == c["domain"]:
                    public_zone = idx
            output = f"""
module "redirect_ns_{c["id"]}"{{
  source = "../../redbaron/modules/godaddy/redirect-nameservers"
  domain = "{c["domain"]}"
  nameservers = module.public_zone.name_servers[{public_zone}]
}}
"""
        return output
    ####################################################################################
    # REDIRECTOR:
    ####################################################################################
    def create_redirector(self,c):
        if c["provider"] == "digitalocean":
            output = digitalocean.main.redirector(c)
        elif c["provider"] == "aws":
            output = aws.main.redirector(c)
        return output
    ####################################################################################
    # C2:
    ####################################################################################
    def create_c2(self,c):
        if c["provider"] == "digitalocean":
            output = digitalocean.main.c2(c)
        elif c["provider"] == "aws":
            output = aws.main.c2(c)
        return output

    ####################################################################################
    # WEBSERVER:
    ####################################################################################
    def create_webserver(self,c):
        if c["provider"] == "digitalocean":
            output = digitalocean.main.webserver(c)
        elif c["provider"] == "aws":
            output = aws.main.webserver(c)
        return output

    ####################################################################################
    # GOPHISH:
    ####################################################################################
    def create_gophish(self,c):
        if c["provider"] == "digitalocean":
            output = digitalocean.main.gophish(c)
        elif c["provider"] == "aws":
            output = aws.main.gophish(c)
        return output

    ####################################################################################
    # DNS_NAMES
    ####################################################################################
    def create_dns_names(self):
        output=""
        if len(self.aws_domains ) != 0:
            domain_string_aws = ', '.join('"{0}"'.format(d) for d in  self.aws_domains)
            output = output + aws.main.create_dns_name(domain_string_aws)
        return output

    ####################################################################################
    # CERTIFICATES:
    ####################################################################################
    def create_cert(self,c):
        for camp in self.campaign:
            if camp["id"] == c["mod_id"].split('-')[0]:
                if camp["provider"] == "digitalocean":
                    if camp["module"] == "gophish":
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/digitalocean/create-cert-dns-gophish-do"
  provider_name = "digitalocean"
  server_url = "production" #"staging" #"production" #(change this for live)
  domain = "{c["domain_name"]}"
  do_token = var.do_token
  phishing_server_ip = module.{camp["module"]}_{camp["id"]}.ips[0][0]
}}
"""
                    elif camp["module"] == "webserver":
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/digitalocean/create-cert-webserver-do"
  domain = "{c["domain_name"]}"
  phishing_server_ip = module.{camp["module"]}_{camp["id"]}.ips[0][0]
}}
"""
                    elif camp["module"] == "c2" or ():
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/digitalocean/create-cert-dns-do"
  provider_name = "digitalocean"
  server_url = "production" #"staging" #"production" #(change this for live)
  domain = "{c["domain_name"]}"
  do_token = var.do_token
}}
"""
                    elif camp["module"] == "redirector" and camp["redirector_id"] == "localhost" :
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/digitalocean/create-cert-dns-do"
  provider_name = "digitalocean"
  server_url = "production" #"staging" #"production" #(change this for live)
  domain = "{c["domain_name"]}"
  do_token = var.do_token
}}
"""

#AWS
                if camp["provider"] == "aws":
                    public_zone = 0
                    for idx,d in enumerate(self.aws_domains):
                        if d == c["domain_name"]:
                            public_zone = idx

                    if camp["module"] == "gophish":
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/aws/create-cert-dns-gophish-aws"
  domain = "{c["domain_name"]}"
  aws_key = var.aws_key
  aws_secret = var.aws_secret
  region = var.aws_region
  zone = "${{module.public_zone.public_zones_ids[{public_zone}]}}"
  server_url = "production"
  phishing_server_ip = module.{camp["module"]}_{camp["id"]}.ips[0][0]
}}
"""
                    elif camp["module"] == "webserver":
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/aws/create-cert-webserver-aws"
  domain = "{c["domain_name"]}"
  phishing_server_ip = module.{camp["module"]}_{camp["id"]}.ips[0][0]
}}
"""
                    elif camp["module"] == "c2":
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/aws/create-cert-dns-aws"
  server_url = "production" #"staging" #"production" #(change this for live)
  domain = "{c["domain_name"]}"
  aws_key = var.aws_key
  aws_secret = var.aws_secret
  region = var.aws_region
  zone = "${{module.public_zone.public_zones_ids[{public_zone}]}}"
}}
"""
                    elif camp["module"] == "redirector" and camp["redirector_id"] == "localhost" :
                        output=f"""
module "create_cert_{c["id"]}" {{
  source = "../../redbaron/modules/letsencrypt/aws/create-cert-dns-aws"
  server_url = "production" #"staging" #"production" #(change this for live)
  domain = "{c["domain_name"]}"
  aws_key = var.aws_key
  aws_secret = var.aws_secret
  region = var.aws_region
  zone = "${{module.public_zone.public_zones_ids[{public_zone}]}}"
}}
"""
        return output

    ####################################################################################
    # RECORDS:
    ####################################################################################
    def create_dns_records_type(self,c):
        for k in c["records"].keys():
            key = k
        value = c["records"][key]
        record = ""
        output = ""
        if c["provider"] == "digitalocean":
            if c["type"] == "A":
                if len(value.split('-')) > 1:
                    for camp in self.campaign:
                        if camp["id"] == value.split('-')[0]:
                            record = f""" "{key}" = module.{camp["module"]}_rdir_{value.split('-')[0]}.ips[0][{str(int(value.split('-',1)[1])-1)}]"""
                            break
                else:
                    for camp in self.campaign:
                        if camp["id"] == value:
                            record = f""" "{key}" = module.{camp["module"]}_{value}.ips[0][0] """
                            break
            if c["type"] == "MX" or c["type"] == "TXT":
                record = f""" "{key}" = "{value}" """

            output = digitalocean.main.dns_records_type(c,record)
            return output
        elif c["provider"] == "aws":
            if c["type"] == "A":
                if len(value.split('-')) > 1:
                    for camp in self.campaign:
                        if camp["id"] == value.split('-')[0]: #TODO - AWS does not work with more than one redirectors 
                            record = f""" "{key}" = module.{camp["module"]}_rdir_{value.split('-')[0]}.ips[{str(int(value.split('-',1)[1])-1)}] """
                            break
                else:
                    for camp in self.campaign:
                        if camp["id"] == value:
                            record = f""" "{key}" = module.{camp["module"]}_{value}.ips[0] """
                            break
                value = self.aws_domains.index(key)
                output = aws.main.dns_records_type(c,record,value)
                return output
            if c["type"] == "MX":
                record = f""" "{key}" = ["{c["priority"]} {value}"] """
                value = self.aws_domains.index(key)
                output = aws.main.dns_records_type(c,record,value)
                return output
            if c["type"] == "TXT":
                txt_rec_list = []
                txt_rec_list = [""] * len(self.aws_domains)
                if not self.txt_recs:
                    self.txt_recs = True
                    for camp in self.campaign:
                        if camp["module"] == "dns_record" and camp["provider"] == "aws" and camp["type"] == "TXT":
                            for k in camp["records"].keys():
                                key = k
                            value = camp["records"][key]
                            txt_rec_list[self.aws_domains.index(key)] = txt_rec_list[self.aws_domains.index(key)] +" , \""+value +"\""

                    #Replace 3 fist characters in the list
                    output = ""
                    for idx,t in enumerate(txt_rec_list):
                        if len(t) != 0:
                            txt_rec_list[idx] = t[3:]
                            output = output + aws.main.dns_records_type_txt(txt_rec_list[idx],idx)
                    return output
                else:
                    return output


    ####################################################################################
    # MAIL:
    ####################################################################################
    def create_mail(self,c):
        my_nets = []
        for i in c["allowed_ips"]:
            if "." in i:
                my_nets.insert(len(my_nets),i)
            for camp in self.campaign:
                if camp["id"] in i:
                    if "-" in i:
                        my_nets.insert(len(my_nets),('${module.'+camp["module"]+"_"+"rdir_"+camp["id"]+".ips[0]["+str(int(i.split('-')[1])-1)+"]}"))
                        break
                    else:
                        my_nets.insert(len(my_nets),('${module.'+camp["module"]+"_"+camp["id"]+".ips[0][0]}"))
                        break
        my_nets_1 = ' '.join("{0}".format(s) for s in my_nets)
        my_nets_2 = ', '.join("'{0}'".format(s) for s in my_nets)
        my_nets_3 = '\\n'.join("{0}".format(s) for s in my_nets)

        if c["provider"] == "digitalocean":
            output = digitalocean.main.mail(c,my_nets_1,my_nets_2,my_nets_3,self.project_id)
        elif c["provider"] == "aws":
            output = aws.main.mail(c,my_nets_1,my_nets_2,my_nets_3,self.project_id)
        return output
    ####################################################################################
    # Ansible:
    ####################################################################################
    def create_ansible(self,c):
        output = ""
        user = "root"
        for host in c["hosts"]:
            if "-" in host:
                for mod in self.campaign:
                    if mod["id"] == host.split("/")[0].split("-")[0]:
                        if mod["provider"] == "aws":
                            user = "admin"
                        elif mod["provider"] == "digitalocean":
                            user = "root"
                output += f"""
module "ansible_{host.split("/")[0]}_{c["id"]}" {{
source    = "../../redbaron/modules/ansible"
user      = "{user}"
ip        = module.{host.split("/")[1]}_rdir_{host.split("/")[0].split("-")[0]}.ips[0][{int(host.split("/")[0].split("-")[1]) - 1}]
playbook  = "../../redbaron/data/playbooks/{c["playbook"]}"
}}
"""
            else:
                for mod in self.campaign:
                    if mod["id"] == host.split("/")[0]:
                        if mod["provider"] == "aws":
                            if mod["module"] != "c2": # Support for other providers only on c2 at the moment
                                user = "admin"
                            elif mod["distro"] == "debian":
                                user = "admin"
                            elif mod["distro"] == "kali":
                                user = "ec2-user"
                            elif mod["distro"] == "ubuntu":
                                user = "ubuntu"
                        elif mod["provider"] == "digitalocean":
                            user = "root"

                output += f"""
module "ansible_{host.split("/")[0]}_{c["id"]}" {{
source    = "../../redbaron/modules/ansible"
user      = "{user}"
ip        = module.{host.split("/")[1]}_{host.split("/")[0]}.ips[0][0]
playbook  = "../../redbaron/data/playbooks/{c["playbook"]}"
}}
"""
        return output
