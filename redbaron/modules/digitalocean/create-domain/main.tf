# Add a record to the domain
resource "digitalocean_domain" "default" {
  count = var.counter
  name  = var.name[count.index]
}

