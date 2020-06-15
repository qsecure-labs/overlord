output "ips" {
  value = digitalocean_droplet.mail-server.*.ipv4_address
}

output "ssh_user" {
  value = "root"
}

