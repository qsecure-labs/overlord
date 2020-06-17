# Add a record to the domain
resource "digitalocean_record" "record" {
  name     = var.name
  count    = var.counter
  domain   = var.domain
  type     = var.type
  value    = var.records[element(keys(var.records), count.index)]
  ttl      = var.ttl
  priority = var.priority
}

