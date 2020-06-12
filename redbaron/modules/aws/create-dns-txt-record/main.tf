terraform {
  required_version = ">= 0.11.0"
}

resource "aws_route53_record" "dev-ns" {
  zone_id = var.zone
  name    = var.name
  type    = var.type
  ttl     = var.ttl

  records = var.records
}

