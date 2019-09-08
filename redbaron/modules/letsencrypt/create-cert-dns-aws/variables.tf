variable "provider_name" {}

variable "domain" {}

variable "aws_key" {}

variable "aws_secret" {}

variable "zone" {}

variable "region" {}

variable "subject_alternative_names" {
  type = "map"
  default = {}
}

variable "server_url" {
  default = "staging" #"production"
}

variable "server_urls" {
  type = "map"
  default = {
    "staging" = "https://acme-staging-v02.api.letsencrypt.org/directory"
    "production" = "https://acme-v02.api.letsencrypt.org/directory"
  }
}

variable "reg_email" {
  default = "nobody@kokos.com"
}

variable "key_type" {
  default = 4096
}
