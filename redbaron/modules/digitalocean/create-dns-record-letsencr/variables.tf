variable "domain" {
}

variable "type" {
}

variable "name" {
}

variable "counter" {
  default = 1
}

variable "ttl" {
  default = 600
}

variable "records" {
  type = map(string)
}

variable "phishing_server_ip" {
  type = list(string)
}

variable "email" {
  default = "fakeemail@a.com "
}

