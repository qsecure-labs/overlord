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
    provider = var.provider_name

    config = {
      DO_AUTH_TOKEN = var.do_token
    }
  }

  provisioner "local-exec" {
    command = "echo \"${self.private_key_pem}\" > ../../redbaron/data/certificates/${self.common_name}_privkey.pem && echo \"${self.certificate_pem}\" > ../../redbaron/data/certificates/${self.common_name}_cert.pem"
  }

  provisioner "file" {
    source      = "../../redbaron/data/certificates/${var.domain}_privkey.pem"
    destination = "/opt/goapps/src/github.com/gophish/gophish/${var.domain}_privkey.pem"
    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "root"
      private_key = file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "file" {
    source      = "../../redbaron/data/certificates/${var.domain}_cert.pem"
    destination = "/opt/goapps/src/github.com/gophish/gophish/${var.domain}_cert.pem"
    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "root"
      private_key = file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sed -i 's/false/true/g' /opt/goapps/src/github.com/gophish/gophish/config.json",
      "sed -i 's/0.0.0.0:80/0.0.0.0:443/g' /opt/goapps/src/github.com/gophish/gophish/config.json",
      "sed -i 's/example.crt/${var.domain}_cert.pem/g' /opt/goapps/src/github.com/gophish/gophish/config.json",
      "sed -i 's/example.key/${var.domain}_privkey.pem/g' /opt/goapps/src/github.com/gophish/gophish/config.json",
      "systemctl stop gophish.service",
      "systemctl start gophish.service",
    ]

    connection {
      host        = var.phishing_server_ip
      type        = "ssh"
      user        = "root"
      private_key = file("../../redbaron/data/ssh_keys/${var.phishing_server_ip}")
    }
  }

  provisioner "local-exec" {
    when    = destroy
    command = "rm ../../redbaron/data/certificates/${self.common_name}*"
  }
}

