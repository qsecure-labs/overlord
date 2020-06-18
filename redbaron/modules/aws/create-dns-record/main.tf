# Add a record to the domain
resource "aws_route53_record" "record" {
  count   = var.counter
  zone_id = var.zone
  name    = var.name
  type    = var.type
  ttl     = var.ttl
  records = var.records[element(keys(var.records), count.index)]
}

