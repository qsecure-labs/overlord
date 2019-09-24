class main():

    #Redirector
    def redirector(c):
        output = f"""
module "redirector_{c["id"]}" {{
    counter = 1
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = "${{module.{c["redirector_id"].split("/")[1]}_{c["redirector_id"].split("/")[0]}.ips}}"
}}
output "redirector_{c["id"]}-ips" {{
  value = "${{module.redirector_{c["id"]}.ips}}"
}}
"""
        return output

    #C2
    def c2(c):
        scripts = ', '.join('"../../redbaron/data/scripts/tools/{0}.sh"'.format(s) for s in c["tools"])
        if c["redirectors"] > 0:
            output = f"""
module "c2_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-c2"
    install = [{scripts}]
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
}}

module "c2_rdir_{c["id"]}" {{
    counter = {c["redirectors"]}
    source = "../../redbaron/modules/{c["provider"]}/{c["type"]}-rdir"
    redirect_to = "${{module.c2_{c["id"]}.ips}}"
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
    redirect_to = "${{module.webserver_{c["id"]}.ips}}"
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
    redirect_to = "${{module.gophish_{c["id"]}.ips}}"
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
    def mail(c,my_nets_1,my_nets_2):
        output=f"""
module "mail_{c["id"]}" {{
    source = "../../redbaron/modules/{c["provider"]}/mail-server"
    name = "{c["subdomain"]}.{c["domain_name"]}"
    size = "{c["size"]}"
    regions = ["{c["region"]}"]
}}

output "mail-{c["id"]}-ips" {{
  value = "${{module.mail_{c["id"]}.ips}}"
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
      "sudo /etc/init.d/postfix restart",
      "sudo /etc/init.d/clamav-daemon stop",
      "sudo /etc/init.d/clamav-freshclam stop",
      "sudo /etc/init.d/amavis stop",
      "sudo update-rc.d -f clamav-daemon remove",
      "sudo update-rc.d -f clamav-freshclam remove",
      "sudo update-rc.d -f amavis remove",
      "sudo service postfix restart",
      # "service iredapad restart"
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
        output=f"""
module "create_dns_record_{c["id"]}" {{
    source = "../../redbaron/modules/digitalocean/create-dns-record"
    name  = "{c["name"]}"
    type = "{c["type"]}"
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
