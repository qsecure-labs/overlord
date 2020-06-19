resource "godaddy_domain_record" "gd-fancy-domain" {
  domain = var.domain
  nameservers = var.nameservers
}

