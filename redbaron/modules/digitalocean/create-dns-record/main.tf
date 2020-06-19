# Add a record to the domain
resource "digitalocean_domain" "default" {
  name  = var.domain
}

# Add a record to the domain
resource "digitalocean_record" "record" {
  name     = var.name
  count    = var.counter
  domain   = digitalocean_domain.default.name
  type     = var.type
  value    = var.records[element(keys(var.records), count.index)]
  ttl      = var.ttl
  priority = var.priority
}

