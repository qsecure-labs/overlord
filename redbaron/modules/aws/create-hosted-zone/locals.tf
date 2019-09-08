# -------------------------------------------------------------------------------------------------
# Booleans to determine which resource "type" to build
# -------------------------------------------------------------------------------------------------

locals {
  is_name_delegated = "${var.delegation_set_name != "" && var.delegation_set_id == "" ? true : false}"
  is_id_delegated   = "${var.delegation_set_name == "" && var.delegation_set_id != "" ? true : false}"
  is_undelegated    = "${var.delegation_set_name == "" && var.delegation_set_id == "" ? true : false}"
  is_custom_ns      = "${length(var.custom_subdomain_ns) != 0 ? true : false}"
}

# -------------------------------------------------------------------------------------------------
# Split Domains from Subdomains in hosted zones
# -------------------------------------------------------------------------------------------------

locals {
  # The following will split out domains and subdomains from public hosted zones as both require
  # different configuration. Subdomains will also need NS server to be specified.
  #
  # Compact will remove any empty elements (previously included either domains or subdomains)
  # flatten will convert [map('key' => val),..] into flat list without 'key'
  public_domains = "${compact(flatten(null_resource.public_domains.*.triggers.key))}"

  public_subdomains = "${compact(flatten(null_resource.public_subdomains.*.triggers.key))}"
}

resource "null_resource" "public_domains" {
  count = "${length(var.public_hosted_zones)}"

  triggers = "${map("key",
    replace(
      var.public_hosted_zones[count.index],
      "/^[-_A-Za-z0-9]+\\.[A-Za-z0-9]+$/",
      ""
    ) == "" ? var.public_hosted_zones[count.index] : ""
  )}"
}

resource "null_resource" "public_subdomains" {
  count = "${length(var.public_hosted_zones)}"

  triggers = "${map("key",
    replace(
      var.public_hosted_zones[count.index],
      "/^[-_A-Za-z0-9]+\\.[A-Za-z0-9]+$/",
      ""
    ) == "" ? "" : var.public_hosted_zones[count.index]
  )}"
}

# -------------------------------------------------------------------------------------------------
# Resource local mappings for outputs
# -------------------------------------------------------------------------------------------------


#locals {
#    name_delegated_public_domains_ns = ["${null_resource.name_delegated_public_domains_ns.*.triggers.key}"]
#    id_delegated_public_domains_ns   = ["${null_resource.id_delegated_public_domains_ns.*.triggers.key}"]
#    undelegated_public_domains_ns    = ["${null_resource.undelegated_public_domains_ns.*.triggers.key}"]
#
#    name_delegated_public_subdomains_ns = ["${null_resource.name_delegated_public_subdomains_ns.*.triggers.key}"]
#    id_delegated_public_subdomains_ns   = ["${null_resource.id_delegated_public_subdomains_ns.*.triggers.key}"]
#    undelegated_public_subdomains_ns    = ["${null_resource.undelegated_public_subdomains_ns.*.triggers.key}"]
#}
#
#resource "null_resource" "name_delegated_public_domains_ns" {
#  count = "${local.is_name_delegated ? length(local.public_domains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.name_delegated_public_domains.*.name_servers[count.index])
#  )}"
#}
#
#resource "null_resource" "id_delegated_public_domains_ns" {
#  count = "${local.is_id_delegated ? length(local.public_domains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.id_delegated_public_domains.*.name_servers[count.index])
#  )}"
#}
#
#resource "null_resource" "undelegated_public_domains_ns" {
#  count = "${local.is_undelegated ? length(local.public_subdomains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.undelegated_public_subdomains.*.name_servers[count.index])
#  )}"
#}
#
#resource "null_resource" "name_delegated_public_subdomains_ns" {
#  count = "${local.is_name_delegated ? length(local.public_subdomains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.name_delegated_public_subdomains.*.name_servers[count.index])
#  )}"
#}
#
#resource "null_resource" "id_delegated_public_subdomains_ns" {
#  count = "${local.is_id_delegated ? length(local.public_subdomains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.id_delegated_public_subdomains.*.name_servers[count.index])
#  )}"
#}
#
#resource "null_resource" "undelegated_public_subdomains_ns" {
#  count = "${local.is_undelegated ? length(local.public_subdomains) : 0}"
#
#  triggers = "${map("key",
#    join(",", aws_route53_zone.undelegated_public_subdomains.*.name_servers[count.index])
#  )}"
#}
