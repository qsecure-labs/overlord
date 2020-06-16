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
  type    = map(any)
  default = {}
}

variable "zone" {
}

