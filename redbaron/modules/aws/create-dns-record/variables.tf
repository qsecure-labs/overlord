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
  default = {}
}

variable "txt_records" {
  type = "list"
  default = []
}

variable "priority" {
  default = "10"
}

variable "zone" {}
