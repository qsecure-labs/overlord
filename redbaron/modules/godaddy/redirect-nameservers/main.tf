terraform {
  required_version = ">= 0.11.0"
}

resource "godaddy_domain_record" "gd-fancy-domain" {
  domain = "${var.domain}"

  # // specify any custom nameservers for your domain
  nameservers = ["${var.nameservers}"]
}
