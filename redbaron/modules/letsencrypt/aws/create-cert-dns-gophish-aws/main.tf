provider "acme" {
  server_url = var.server_urls[var.server_url]
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "acme_registration" "reg" {
  account_key_pem = tls_private_key.private_key.private_key_pem
  email_address   = var.reg_email
}

resource "acme_certificate" "certificate" {
  account_key_pem = acme_registration.reg.account_key_pem
  common_name     = var.domain

  dns_challenge {
    provider = "route53"

    config = {
      AWS_ACCESS_KEY_ID     = var.aws_key
      AWS_SECRET_ACCESS_KEY = var.aws_secret
      AWS_REGION            = var.region
      AWS_HOSTED_ZONE_ID    = var.zone
    }
  }

  provisioner "local-exec" {
    command = "echo \"${self.private_key_pem}\" > certificates/${self.common_name}_privkey.pem && echo \"${self.certificate_pem}\" > certificates/${self.common_name}_cert.pem"
  }

  provisioner "file" {
    source      = "certificates/${var.domain}_privkey.pem"
    destination = "/tmp/${var.domain}_privkey.pem"
    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "admin"
      private_key = file("ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "file" {
    source      = "certificates/${var.domain}_cert.pem"
    destination = "/tmp/${var.domain}_cert.pem"
    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "admin"
      private_key = file("ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo cp /tmp/${var.domain}_privkey.pem /opt/gophish/${var.domain}_privkey.pem",
      "sudo cp /tmp/${var.domain}_cert.pem /opt/gophish/${var.domain}_cert.pem",
      "sudo sed -i 's/false/true/g' /opt/gophish/config.json",
      "sudo sed -i 's/0.0.0.0:80/0.0.0.0:443/g' /opt/gophish/config.json",
      "sudo sed -i 's/example.crt/${var.domain}_cert.pem/g' /opt/gophish/config.json",
      "sudo sed -i 's/example.key/${var.domain}_privkey.pem/g' /opt/gophish/config.json",
      "sudo sed -i 's/gophish_admin.crt/${var.domain}_cert.pem/g' /opt/gophish/config.json",
      "sudo sed -i 's/gophish_admin.key/${var.domain}_privkey.pem/g' /opt/gophish/config.json",
      "sudo systemctl stop gophish.service",
      "sudo systemctl start gophish.service",
      "sudo rm /opt/gophish/password.txt",
      "sudo cat /var/log/gophish.err | sudo grep 'Please login with the username admin and the password' > /opt/gophish/password.txt"
    ]

    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "admin"
      private_key = file("ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "local-exec" {
    when    = destroy
    command = "rm certificates/${self.common_name}*"
  }
}

