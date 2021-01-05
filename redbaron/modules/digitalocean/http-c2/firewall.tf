data "external" "get_public_ip" {
  program = ["bash", "../../redbaron/data/scripts/get_public_ip.sh"]
}

resource "random_id" "firewall" {
  byte_length = 4
}

resource "digitalocean_firewall" "web" {
  name = "http-c2-only-allow-dns-http-ssh-${random_id.firewall.hex}"

  droplet_ids = digitalocean_droplet.http-c2.*.id

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["${data.external.get_public_ip.result["ip"]}/32"]
  }
  inbound_rule { # Rule for covenant admin panel
    protocol         = "tcp"
    port_range       = "7443"
    source_addresses = ["${data.external.get_public_ip.result["ip"]}/32"]
  }
  inbound_rule { # Rule for cobaltstrike
    protocol         = "tcp"
    port_range       = "50050"
    source_addresses = ["${data.external.get_public_ip.result["ip"]}/32"]
  }
  inbound_rule {
    protocol         = "udp"
    port_range       = "60000-61000"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "udp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "tcp"
    port_range            = "443"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "tcp"
    port_range            = "80"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

