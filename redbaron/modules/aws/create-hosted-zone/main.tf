# -------------------------------------------------------------------------------------------------
# Create delegation set or gather existing one
# -------------------------------------------------------------------------------------------------
resource "aws_route53_delegation_set" "new" {
  count = local.is_name_delegated ? 1 : 0

  reference_name = var.delegation_set_name
}

data "aws_route53_delegation_set" "existing" {
  count = local.is_id_delegated ? 1 : 0

  id = var.delegation_set_id
}

# -------------------------------------------------------------------------------------------------
# [Domains 1/3] Public Hosted Zones for Domains with delegation-set name
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "name_delegated_public_domains" {
  count = local.is_name_delegated ? length(local.public_domains) : 0

  name    = local.public_domains[count.index]
  comment = var.comment

  delegation_set_id = aws_route53_delegation_set.new[0].id

  tags = merge(
    {
      "Name" = local.public_domains[count.index]
    },
    {
      "Route53Delegated" = "yes"
    },
    {
      "Route53DelegationName" = var.delegation_set_name
    },
    {
      "Route53Type" = "domain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [Domains 2/3] Public Hosted Zones for Domains with delegation-set ID
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "id_delegated_public_domains" {
  count = local.is_id_delegated ? length(local.public_domains) : 0

  name    = local.public_domains[count.index]
  comment = var.comment

  delegation_set_id = var.delegation_set_id

  tags = merge(
    {
      "Name" = local.public_domains[count.index]
    },
    {
      "Route53Delegated" = "yes"
    },
    {
      "Route53DelegationId" = var.delegation_set_id
    },
    {
      "Route53Type" = "domain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [Domains 3/3] Public Hosted Zones for Domains without any delegation
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "undelegated_public_domains" {
  count = local.is_undelegated ? length(local.public_domains) : 0

  name    = local.public_domains[count.index]
  comment = var.comment

  tags = merge(
    {
      "Name" = local.public_domains[count.index]
    },
    {
      "Route53Delegated" = "no"
    },
    {
      "Route53Type" = "domain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [Subdomains 1/3] Public Hosted Zones for Subomains with delegation-set name
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "name_delegated_public_subdomains" {
  count = local.is_name_delegated ? length(local.public_subdomains) : 0

  name    = local.public_subdomains[count.index]
  comment = var.comment

  delegation_set_id = aws_route53_delegation_set.new[0].id

  tags = merge(
    {
      "Name" = local.public_subdomains[count.index]
    },
    {
      "Route53Delegated" = "yes"
    },
    {
      "Route53DelegationName" = var.delegation_set_name
    },
    {
      "Route53Type" = "subdomain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [Subdomains 2/3] Public Hosted Zones for Subomains with delegation-set ID
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "id_delegated_public_subdomains" {
  count = local.is_id_delegated ? length(local.public_subdomains) : 0

  name    = local.public_subdomains[count.index]
  comment = var.comment

  delegation_set_id = var.delegation_set_id

  tags = merge(
    {
      "Name" = local.public_subdomains[count.index]
    },
    {
      "Route53Delegated" = "yes"
    },
    {
      "Route53DelegationId" = var.delegation_set_id
    },
    {
      "Route53Type" = "subdomain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [Subdomains 3/3] Public Hosted Zones for Subomains without any delegation
# -------------------------------------------------------------------------------------------------
resource "aws_route53_zone" "undelegated_public_subdomains" {
  count = local.is_undelegated ? length(local.public_subdomains) : 0

  name    = local.public_subdomains[count.index]
  comment = var.comment

  tags = merge(
    {
      "Name" = local.public_subdomains[count.index]
    },
    {
      "Route53Delegated" = "no"
    },
    {
      "Route53Type" = "subdomain"
    },
    var.tags,
  )
}

# -------------------------------------------------------------------------------------------------
# [NS Records 1/3] Public Hosted Zone Subdomain NS Records with delegation-set name
# -------------------------------------------------------------------------------------------------
resource "aws_route53_record" "name_delegated_subdomains_ns_default" {
  count = local.is_name_delegated && false == local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.name_delegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = aws_route53_zone.name_delegated_public_subdomains[count.index].name_servers
}

resource "aws_route53_record" "name_delegated_subdomains_ns_custom" {
  count = local.is_name_delegated && local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.name_delegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = var.custom_subdomain_ns
}

# -------------------------------------------------------------------------------------------------
# [NS Records 2/3] Public Hosted Zone Subdomain NS Records with existing delegation-set ID
# -------------------------------------------------------------------------------------------------
resource "aws_route53_record" "id_delegated_subdomains_ns_default" {
  count = local.is_id_delegated && false == local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.id_delegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = aws_route53_zone.id_delegated_public_subdomains[count.index].name_servers
}

resource "aws_route53_record" "id_delegated_subdomains_ns_custom" {
  count = local.is_id_delegated && local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.id_delegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = var.custom_subdomain_ns
}

# -------------------------------------------------------------------------------------------------
# [NS Records 3/3] Public Hosted Zone Subdomain NS Records without any delegation
# -------------------------------------------------------------------------------------------------
resource "aws_route53_record" "undelegated_subdomains_ns_default" {
  count = local.is_undelegated && false == local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.undelegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = aws_route53_zone.undelegated_public_subdomains[count.index].name_servers
}

resource "aws_route53_record" "undelegated_subdomains_ns_custom" {
  count = local.is_undelegated && local.is_custom_ns ? length(local.public_subdomains) : 0

  zone_id = aws_route53_zone.undelegated_public_subdomains[count.index].zone_id
  name    = local.public_subdomains[count.index]
  type    = "NS"
  ttl     = var.default_subdomain_ns_ttl

  records = var.custom_subdomain_ns
}

