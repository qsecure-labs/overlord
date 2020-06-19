output "ips" {
  value = [aws_instance.gophish-server.*.public_ip]
}

