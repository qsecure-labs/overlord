output "ips" {
  value = [digitalocean_droplet.mail-server.*.ipv4_address]
}