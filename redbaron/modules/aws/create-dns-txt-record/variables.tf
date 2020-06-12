variable "type" {}

variable "name" {}

variable "ttl" {
  default = 600
}

variable "records" {
  type = "list"
  default = []
}

variable "zone" {}
