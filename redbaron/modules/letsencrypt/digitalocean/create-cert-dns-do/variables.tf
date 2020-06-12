variable "provider_name" {
}

variable "do_token" {
  
}
variable "domain" {
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
