class main():

    #Redirector
    def redirector(c):
        if c["redirector_id"] == "localhost" and c["type"]== "dns":
          output = f"""
module "redirector_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-local-rdir"
    redirect_to = ["localhost"]
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
output "{c["id"]}_Run_the_following_command_on_your_internal_HTTP_server" {{
  value = "\\n\\nsocat tcp4-LISTEN:53,fork udp:localhost:53\\nsudo autossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 2222:localhost:53 admin@${{module.redirector_{c["id"]}.ips[0][0]}}\\n"
}}
""" 
        elif c["redirector_id"] == "localhost" and c["type"]== "http":
          output = f"""
module "redirector_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = ["localhost"]
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
    http-port = 8080
    https-port = 4443
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
output "{c["id"]}_Run_the_following_command_on_your_internal_HTTP_server" {{
  value = "\\n\\nautossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 8080:localhost:80 admin@${{module.redirector_{c["id"]}.ips[0][0]}}\\nautossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 4443:localhost:443 admin@${{module.redirector_{c["id"]}.ips[0][0]}}\\n"
}}
"""        
        else:
          output = f"""
module "redirector_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = flatten("${{module.{c["redirector_id"].split("/")[1]}_{c["redirector_id"].split("/")[0]}.ips}}")
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
"""
        return output

    #C2
    def c2(c):
        scripts = ', '.join('"../../redbaron/data/scripts/tools/{0}.sh"'.format(s) for s in c["tools"])
        user = ""
        if c["distro"] == "kali":
          user = "ec2-user"
        elif c["distro"] == "ubuntu":
          user = "ubuntu"
        else:
          user = "admin"
        
        if c["redirectors"] > 0:
            output = f"""
module "c2_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-c2"
    install = [{scripts}]
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
    user = "{user}"
    amis = {{"{c["region"]}"="{c["ami"]}"}}
}}

module "c2_rdir_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = flatten("${{module.c2_{c["id"]}.ips}}")
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

output "c2-{c["id"]}-ips" {{
  value = "${{module.c2_{c["id"]}.ips}}"
}}

output "c2-rdir-{c["id"]}-ips" {{
  value = "${{module.c2_rdir_{c["id"]}.ips}}"
}}

"""
        else:
                output = f"""
module "c2_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-c2"
    install = [{scripts}]
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
    user = "{user}"
    amis = {{"{c["region"]}"="{c["ami"]}"}}
}}

output "c2-{c["id"]}-ips" {{
  value = "${{module.c2_{c["id"]}.ips}}"
}}
"""
        return output

    #WebServer
    def webserver(c):
        if c["redirectors"] > 0:
            output = f"""
module "webserver_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/phishing-server"
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

module "webserver_rdir_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/http-rdir"
    redirect_to = flatten("${{module.webserver_{c["id"]}.ips}}")
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

output "webserver-{c["id"]}-ips" {{
  value = "${{module.webserver_{c["id"]}.ips}}"
}}

output "webserver-rdir-{c["id"]}-ips" {{
  value = "${{module.webserver_rdir_{c["id"]}.ips}}"
}}

"""
        else:
            output = f"""
module "webserver_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/phishing-server"
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

output "webserver-{c["id"]}-ips" {{
  value = "${{module.webserver_{c["id"]}.ips}}"
}}

"""
        return output

    #Gophish:
    def gophish(c):
        if c["redirectors"] > 0:
            output = f"""
module "gophish_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/phishing-server-gophish"
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

module "gophish_rdir_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/http-rdir"
    redirect_to = flatten("${{module.gophish_{c["id"]}.ips}}")
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

output "gophish-{c["id"]}-ips" {{
  value = "${{module.gophish_{c["id"]}.ips}}"
}}

output "gophish-rdir-{c["id"]}-ips" {{
  value = "${{module.gophish_rdir_{c["id"]}.ips}}"
}}

"""
        else:
            output = f"""
module "gophish_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/phishing-server-gophish"
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
}}

output "gophish-{c["id"]}-ips" {{
  value = "${{module.gophish_{c["id"]}.ips}}"
}}

"""
        return output

    #Mail
    def mail(c,my_nets_1,my_nets_2,my_nets_3,project_id):
        data = ""
        with open (f"projects/{project_id}/{c['id']}/iredmailpass.txt", "r") as myfile:
            data = myfile.readlines()        
        data = data[0].strip('\n')

        output=f"""
module "mail_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/mail-server"
    instance_type = "{c["size"]}"
    vpc_id = "${{module.create_vpc.vpc_id}}"
    subnet_id = "${{module.create_vpc.subnet_id}}"
    path = "{c["id"]}/iredmail.sh"
}}

output "mail-{c["id"]}-ips" {{
  value = "${{module.mail_{c["id"]}.ips}}"
}}

output "iRedMail_credentials_{c["id"]}" {{
  value = "postmaster@{c["domain_name"]}:{data}\\n"
}}

resource "null_resource" "update_iredmail_{c["id"]}" {{

  provisioner "remote-exec" {{
    inline = [
      "sudo postconf -e 'mynetworks = 127.0.0.1 [::1] {my_nets_1}'",
      "echo \\"MYNETWORKS = [{my_nets_2}]\\" | sudo tee -a /opt/iredapd/settings.py",
      "sudo postconf -e \\"mydomain = {c["domain_name"]}\\"",
      "sudo postconf -e \\"myhostname = {c["subdomain"]}.{c["domain_name"]}\\"",
      "sudo postconf -e \\"myorigin = \\\\$mydomain\\"",
      "sudo postconf -# \\"content_filter\\"",
      "sudo postconf -e \\"always_add_missing_headers = yes\\"",
      "sudo sed -i 's/@bypass_virus_checks_maps = (0);/@bypass_virus_checks_maps = (1);/g' /etc/amavis/conf.d/50-user",
      "sudo touch /etc/postfix/sender_access.pcre",
      "sudo echo -e \\"{my_nets_3}\\" | sudo tee -a /etc/postfix/sender_access.pcre",
      "sudo service clamav-daemon restart",
      "sudo service amavis restart",
      "sudo service clamav-freshclam restart",
      "sudo service postfix restart"
    ]

    connection {{
        host = module.mail_{c["id"]}.ips[0][0]
        type = "ssh"
        user = "admin"
        private_key = "${{file("../../redbaron/data/ssh_keys/${{module.mail_{c["id"]}.ips[0][0]}}")}}"
    }}
  }}
}}

"""
        return output

    def dns_records_type(c,record,value):
        if not c["name"]:
          output=f"""
module "create_dns_record_{c["id"]}" {{
    source = "../../redbaron/modules/aws/create-dns-record"
    name  = "{list(c["records"])[0]}"
    type = "{c["type"]}"
    records = {{ {record} }}
    zone = module.public_zone.public_zones_ids[{value}]
}}\n"""
        else:
          output=f"""
module "create_dns_record_{c["id"]}" {{
    source = "../../redbaron/modules/aws/create-dns-record"
    name  = "{c["name"]}.{list(c["records"])[0]}"
    type = "{c["type"]}"
    records = {{ {record} }}
    zone = module.public_zone.public_zones_ids[{value}]
}}\n"""
        return output


    def dns_records_type_txt(record,value):
        output=f"""
module "create_dns_record_{value}" {{
    source = "../../redbaron/modules/aws/create-dns-txt-record"
    name  = ""
    type = "TXT"
    records = [{record}]
    zone = module.public_zone.public_zones_ids[{value}]
}}\n"""
        return output

    def create_dns_name(domain_string_aws):
        output=f"""
##################################################################################################################
#                                          DNS ROUTE53 Zone                                                      #
##################################################################################################################
module "public_zone" {{
  source = "../../redbaron/modules/aws/create-hosted-zone"

  public_hosted_zones = [{domain_string_aws}]
  tags = {{
    Environment    = "prod"
    Infrastructure = "core"
    Owner          = "terraform"
    Project        = "zones-public"
  }}

  comment = "Managed by Terraform"
}}
"""
        return output

