terraform {
  required_version = ">= 0.11.0"
}

# Add a record to the domain
resource "digitalocean_domain" "default" {
  count = var.counter
  name  = var.name[count.index]
}

