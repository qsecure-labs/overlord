variable "domain" {}

variable "type" {}

variable "counter" {
  default = 1
}

variable "ttl" {
  default = 600
}

variable "records" {
  type = "map"
}
