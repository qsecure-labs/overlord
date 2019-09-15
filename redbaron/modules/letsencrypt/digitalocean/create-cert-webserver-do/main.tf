
resource "null_resource" "lets-encrypt" {
  count  = "${var.counter}"
  provisioner "remote-exec" {
    inline = [
      "certbot --apache --non-interactive --agree-tos --email ${var.email} --domain ${var.domain} --pre-hook 'sudo service apache2 stop' --post-hook 'sudo service apache2 start' --dry-run", #--dry-run is for staging not production chage this
      "certbot renew --dry-run"
    ]

    connection {
        host = "${var.phishing_server_ip}"
        type = "ssh"
        user = "root"
        private_key = "${file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")}"
    }
  }
}



# Resource for lets-encrypt with multiple domains
#resource "null_resource" "lets-encrypt" {
#   count  = "${var.counter}"
#   provisioner "remote-exec" {
#     inline = [
#       "certbot --apache --non-interactive --agree-tos --email ${var.email} --domain ${element(var.domains, count.index)} --pre-hook 'sudo service apache2 stop' --post-hook 'sudo service apache2 start'",
#       "certbot renew --dry-run"
#     ]

#     connection {
#         host = "${element(var.phishing_server_ip, count.index)}"
#         type = "ssh"
#         user = "root"
#         private_key = "${file("../../redbaron/data/ssh_keys/${element(var.phishing_server_ip, count.index)}")}"
#     }
#   }
# }
