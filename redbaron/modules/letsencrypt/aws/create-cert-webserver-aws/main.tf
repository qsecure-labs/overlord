resource "null_resource" "lets-encrypt" {
  provisioner "remote-exec" {
    inline = [
      "sudo certbot --apache --non-interactive --agree-tos --email ${var.email} --domain ${var.domain} --pre-hook 'sudo service apache2 stop' --post-hook 'sudo service apache2 start'", #--dry-run is for staging not production chage this
      "sudo certbot renew",
    ]

    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "admin"
      private_key = file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")
    }
  }
}

