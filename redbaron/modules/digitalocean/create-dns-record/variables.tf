variable "type" {
}

variable "name" {
}

variable "domain" {
}

variable "counter" {
  default = 1
}

variable "ttl" {
  default = 600
}

variable "records" {
  type = map(any)
}

variable "priority" {
  default = "10"
}

