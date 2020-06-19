# Add a record to the domain
resource "null_resource" "previous" {}

resource "time_sleep" "wait_60_seconds" {
  depends_on = [null_resource.previous]

  create_duration = "60s"
}

resource "digitalocean_record" "record" {
  name     = var.name
  count    = var.counter
  domain   = var.domain
  type     = var.type
  value    = var.records[element(keys(var.records), count.index)]
  ttl      = var.ttl
  priority = var.priority
  depends_on = [time_sleep.wait_60_seconds]
}

