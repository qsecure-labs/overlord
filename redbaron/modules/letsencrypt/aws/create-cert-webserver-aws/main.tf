resource "null_resource" "lets-encrypt" {
  provisioner "remote-exec" {
    inline = [
      "sudo service apache2 start",
      "sudo wget https://dl.eff.org/certbot-auto",
      "sudo mv certbot-auto /usr/local/bin/certbot-auto",
      "sudo chown root /usr/local/bin/certbot-auto",
      "sudo chmod 0755 /usr/local/bin/certbot-auto",
      "sudo /usr/local/bin/certbot-auto --apache --non-interactive --agree-tos --email ${var.email} --domain ${var.domain}",
      "sudo service apache2 restart"
    ]

    connection {
        host = "${var.phishing_server_ip}"
        type = "ssh"
        user = "admin"
        private_key = "${file("ssh_keys/${var.phishing_server_ip}")}"
    }
  }
}