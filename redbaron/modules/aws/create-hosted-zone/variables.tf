# -------------------------------------------------------------------------------------------------
# Hosted Zone definitions
# -------------------------------------------------------------------------------------------------
variable "public_hosted_zones" {
  description = "List of domains or subdomains for which to create public hosted zones."
  type        = "list"
  default     = []
}

variable "delegation_set_name" {
  description = "Create a shared delegation set among specefied hosted zones domains if not empty. (nmutually exclusive to 'delegation_set_id')."
  default     = ""
}

variable "delegation_set_id" {
  description = "Assign specified hosted zones to a delegation set specified by ID if not empty. (mutually exclusive to 'delegation_set_reference_name')."
  default     = ""
}

variable "custom_subdomain_ns" {
  description = "Hosted zones for subdomains require nameserver to be specified explicitly. You can use this variable to add a list of custom nameserver IP addresses. If left empty it will be populated by four AWS default nameserver."
  type        = "list"
  default     = []
}

variable "default_subdomain_ns_ttl" {
  description = "Hosted zones for subdomains require nameserver to be specified explicitly. This sets their default TTL."
  default     = "30"
}

# -------------------------------------------------------------------------------------------------
# Resource Tagging/Naming
# -------------------------------------------------------------------------------------------------
variable "tags" {
  description = "The resource tags that should be added to all hosted zone resources."
  type        = "map"
  default     = {}
}

variable "comment" {
  description = "The hosted zone comment that should be added to all hosted zone resources."
  default     = "Managed by Terraform"
}
