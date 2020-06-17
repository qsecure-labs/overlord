resource "null_resource" "lets-encrypt" {
  count = var.counter
  provisioner "remote-exec" {
    inline = [
      "certbot --apache --non-interactive --agree-tos --email ${var.email} --domain ${var.domain} --pre-hook 'sudo service apache2 stop' --post-hook 'sudo service apache2 start'", #--dry-run is for staging not production chage this
      "certbot renew",
    ]

    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "root"
      private_key = file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")
    }
  }
}

