variable "domain" {
}

variable "server_url" {
  default = "staging" #"production"
}

variable "aws_key" {
}

variable "aws_secret" {
}

variable "zone" {
}

variable "region" {
}

variable "server_urls" {
  type = map(string)
  default = {
    "staging"    = "https://acme-staging-v02.api.letsencrypt.org/directory"
    "production" = "https://acme-v02.api.letsencrypt.org/directory"
  }
}

variable "reg_email" {
  default = "nobody@kokos.com"
}

variable "phishing_server_ip" {
}

