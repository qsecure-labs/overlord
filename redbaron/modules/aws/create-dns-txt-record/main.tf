# Time delay
resource "null_resource" "previous" {}

resource "time_sleep" "wait_60_seconds" {
  depends_on = [null_resource.previous]

  create_duration = "60s"
}

# Add a TXT record to the domain
resource "aws_route53_record" "dev-ns" {
  zone_id = var.zone
  name    = var.name
  type    = var.type
  ttl     = var.ttl
  records = var.records
  depends_on = [time_sleep.wait_60_seconds]
}

