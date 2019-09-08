variable "domain" {}

variable "type" {}

variable "name" {}

variable "counter" {
  default = 1
}

variable "ttl" {
  default = 600
}

variable "records" {
  type = "map"
}

variable "phishing_server_ip" {
    type = "list"
}

variable "email" {
  default = "fakeemail@a.com "
}
