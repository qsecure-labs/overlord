terraform {
  required_version = ">= 0.11.0"
}

# Add a record to the domain
resource "digitalocean_record" "record" {
  name   = var.name
  count  = var.counter
  domain = element(keys(var.records), count.index)
  type   = var.type
  value  = var.records[element(keys(var.records), count.index)]
  ttl    = var.ttl
}

resource "null_resource" "lets-encrypt" {
  count      = var.counter
  depends_on = [digitalocean_record.record]
  provisioner "remote-exec" {
    inline = [
      "certbot --apache --non-interactive --agree-tos --email ${var.email} --domain ${var.domain} --pre-hook 'sudo service apache2 stop' --post-hook 'sudo service apache2 start'", # --dry-run", # --dry-run is for staging not production remove this on actual attack
      "certbot renew",
    ] # --dry-run"

    connection {
      host = element(var.phishing_server_ip, count.index)
      type = "ssh"
      user = "root"
      private_key = file(
        "../../redbaron/data/ssh_keys/${element(var.phishing_server_ip, count.index)}",
      )
    }
  }
}

