provider "acme" {
  # server_url = "https://acme-v02.api.letsencrypt.org/directory" #"https://acme-staging-v02.api.letsencrypt.org/directory"
  server_url = "https://acme-staging-v02.api.letsencrypt.org/directory"
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "acme_registration" "reg" {
  account_key_pem = "${tls_private_key.private_key.private_key_pem}"
  email_address   = "${var.reg_email}"
}

resource "acme_certificate" "certificate" {
  account_key_pem           = "${acme_registration.reg.account_key_pem}"
  common_name               = "${var.domain}"
  # subject_alternative_names = ["${var.domain[0]}"]

  dns_challenge {
    provider = "route53"

    config {
     AWS_ACCESS_KEY_ID  = "${var.aws_key}"
     AWS_SECRET_ACCESS_KEY = "${var.aws_secret}"
     AWS_REGION = "${var.region}"
     AWS_HOSTED_ZONE_ID = "${var.zone}"
   }
  }

  provisioner "local-exec" {
    command = "echo \"${self.private_key_pem}\" > ../../redbaron/data/certificates/${self.common_name}_privkey.pem && echo \"${self.certificate_pem}\" > ../../redbaron/data/certificates/${self.common_name}_cert.pem"
  }

  provisioner "local-exec" {
    when = "destroy"
    command = "rm ../../redbaron/data/certificates/${self.common_name}*"
  }
}
