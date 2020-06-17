class main():

    #Redirector
    def redirector(c):
        if c["redirector_id"] == "localhost" and c["type"]== "dns":
          output = f"""
module "redirector_{c["id"]}" {{
    counter = 1
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-local-rdir"
    redirect_to = ["{c["redirector_id"]}"]
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
output "{c["id"]}_Run_the_following_command_on_your_internal_HTTP_server" {{
  value = "\\n\\nsocat tcp4-LISTEN:53,fork udp:localhost:53\\nsudo autossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 2222:localhost:53 root@${{module.redirector_{c["id"]}.ips[0][0]}}\\n"
}}
"""
        elif c["redirector_id"] == "localhost" and c["type"]== "http":
          output = f"""
module "redirector_{c["id"]}" {{
    counter = 1
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = ["{c["redirector_id"]}"]
    http-port = 8080
    https-port = 4443
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
output "{c["id"]}_Run_the_following_command_on_your_internal_HTTP_server" {{
  value = "\\n\\nautossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 8080:localhost:80 root@${{module.redirector_{c["id"]}.ips[0][0]}}\\nautossh -M 11166 -i ${{module.redirector_{c["id"]}.ips[0][0]}} -N -R 4443:localhost:443 root@${{module.redirector_{c["id"]}.ips[0][0]}}\\n"
}}
"""
        else:
          output = f"""
module "redirector_{c["id"]}" {{
    counter = 1
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = flatten("${{module.{c["redirector_id"].split("/")[1]}_{c["redirector_id"].split("/")[0]}.ips}}")
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
"""
        return output

    #C2
    def c2(c):
        scripts = ', '.join('"../../redbaron/data/scripts/tools/{0}.sh"'.format(s) for s in c["tools"])
        linux_distro = "debian-9-x64"
        if c["distro"] == "ubuntu":
          linux_distro = "ubuntu-18-04-x64"

        if c["redirectors"] > 0:
            output = f"""
module "c2_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-c2"
    install = [{scripts}]
    size = "{c["size"]}"
    distro = "{linux_distro}"
    regions = ["{c["region"]}"]
}}

module "c2_rdir_{c["id"]}" {{
    counter = {c["redirectors"]}
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = flatten("${{module.c2_{c["id"]}.ips}}")
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
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
}}

output "c2-{c["id"]}-ips" {{
  value = "${{module.c2_{c["id"]}.ips}}"
}}
"""
        return output

    def webserver(c):
        if c["redirectors"] > 0:
            output = f"""
module "webserver_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/phishing-server"
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
}}

module "webserver_rdir_{c["id"]}" {{
    counter = {c["redirectors"]}
    source = "../../redbaron/modules/{c["provider"]}/http-rdir"
    redirect_to = flatten("${{module.webserver_{c["id"]}.ips}}")
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
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
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
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
}}

module "gophish_rdir_{c["id"]}" {{
    counter = {c["redirectors"]}
    source = "../../redbaron/modules/{c["provider"]}/http-rdir"
    redirect_to = flatten("${{module.gophish_{c["id"]}.ips}}")
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
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
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
    name = "{c["subdomain"]}.{c["domain_name"]}"
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
    path = "{c["id"]}/iredmail.sh"
}}

output "mail-{c["id"]}-ips" {{
  value = "${{module.mail_{c["id"]}.ips}}"
}}

output "iRedMail_credentials" {{
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
        host = "${{module.mail_{c["id"]}.ips[0]}}"
        type = "ssh"
        user = "root"
        private_key = "${{file("../../redbaron/data/ssh_keys/${{module.mail_{c["id"]}.ips[0]}}")}}"
    }}
  }}
}}

"""
        return output

    def dns_records_type(c,record):
        domain = record.split('"')
        if "v=DMARC1;" in record:
          c["name"] ="_dmarc"
        output=f"""
module "create_dns_record_{c["id"]}" {{
    source = "../../redbaron/modules/digitalocean/create-dns-record"
    name  = "{c["name"]}"
    type = "{c["type"]}"
    domain = "{domain[1]}"
    priority= {c["priority"]}
    counter = {c["counter"]}
    records = {{ {record} }}
}}\n"""
        return output


    def create_dns_name():
        output= """
###################################################################################################################
#                                          DNS DIGITALOCEAN                                                       #
###################################################################################################################
module "create_domain_name_do" {
    source = "../../redbaron/modules/digitalocean/create-domain"
    counter = "${length("${var.do_domain}")}"
    name = "${var.do_domain}"
}\n"""
        return output

#     def firewall(c):
#       mod, mod_type = c["mod_id"].split('/')
#       output=f"""
# ###################################################################################################################
# #                                          FIREWALL                                                           #
# ###################################################################################################################
# resource "digitalocean_firewall" "{c["id"]}" {{
#   name = "{c["rule"]}_{c["port"]}_{c["id"]}"

#   droplet_ids = ["${{module.{mod_type}_{mod}.id}}"]

#   {c["rule"]}_rule {{
#       protocol           = "{c["protocol"]}"
#       port_range         = "{c["port"]}"
#       source_addresses   = ["0.0.0.0/0", "::/0"]
#   }}
# }}
# """
#       print(output)
#       return output
