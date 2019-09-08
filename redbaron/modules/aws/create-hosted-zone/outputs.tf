# -------------------------------------------------------------------------------------------------
# Route53 Delegation Sets
# -------------------------------------------------------------------------------------------------

output "created_delegation_set_id" {
  description = "The ID of the shared delegation set applied to all zones that has been created by this module if it was specified by name."
  value       = "${element(concat(aws_route53_delegation_set.new.*.id, list("")), 0)}"
}

output "created_delegation_set_name" {
  description = "The name of the shared delegation set applied to all zones that has been created by this module if it was specified by name."
  value       = "${element(concat(aws_route53_delegation_set.new.*.reference_name, list("")), 0)}"
}

output "created_delegation_set_name_servers" {
  description = "A list of name servers of the shared delegation set applied to all zones that has been created by this module if it was specified by name."
  value       = ["${flatten(aws_route53_delegation_set.new.*.name_servers)}"]
}

output "existing_delegation_set_id" {
  description = "The ID of the shared delegation set applied to all zones that alreday existed and was specified by its ID."
  value       = "${element(concat(data.aws_route53_delegation_set.existing.*.id, list("")), 0)}"
}

output "existing_delegation_set_name" {
  description = "The name of the shared delegation set applied to all zones that alreday existed and was specified by its ID."
  value       = "${element(concat(data.aws_route53_delegation_set.existing.*.reference_name, list("")), 0)}"
}

output "existing_delegation_set_name_servers" {
  description = "A list of name servers of the shared delegation set applied to all zones that alreday existed and was specified by its ID."
  value       = ["${flatten(data.aws_route53_delegation_set.existing.*.name_servers)}"]
}

# -------------------------------------------------------------------------------------------------
# Route53 Zone Settings
# -------------------------------------------------------------------------------------------------

output "public_zones_delegation_set_id" {
  description = "The ID of the shared delegation set applied to all zones that is actually used by the zones."
  value       = "${element(concat(aws_route53_delegation_set.new.*.id, data.aws_route53_delegation_set.existing.*.id, list("")), 0)}"
}

output "public_zones" {
  description = "List of created public zones."

  value = [
    "${concat(
      aws_route53_zone.name_delegated_public_domains.*.name,
      aws_route53_zone.id_delegated_public_domains.*.name,
      aws_route53_zone.undelegated_public_domains.*.name,
      aws_route53_zone.name_delegated_public_subdomains.*.name,
      aws_route53_zone.id_delegated_public_subdomains.*.name,
      aws_route53_zone.undelegated_public_subdomains.*.name,
    )}",
  ]
}

output "public_zones_ids" {
  description = "List of zone-id mappings for created public zones."

  value = "${concat(
    formatlist(
    "%v",
      aws_route53_zone.name_delegated_public_domains.*.id,
    ),
    formatlist(
    "%v",
      aws_route53_zone.id_delegated_public_domains.*.id,
    ),
    formatlist(
    "%v",
      aws_route53_zone.undelegated_public_domains.*.id,
    ),
    formatlist(
    "%v",
      aws_route53_zone.name_delegated_public_subdomains.*.id,
    ),
    formatlist(
    "%v",
      aws_route53_zone.id_delegated_public_subdomains.*.id,
    ),
    formatlist(
    "%v",
      aws_route53_zone.undelegated_public_subdomains.*.id,
    ),
  )}"
}

output "name_servers" {
  description = "List of NS mappings for created public zones."

  value = "${concat(
      aws_route53_zone.name_delegated_public_domains.*.name_servers,
      aws_route53_zone.id_delegated_public_domains.*.name_servers,
      aws_route53_zone.undelegated_public_domains.*.name_servers,
      aws_route53_zone.name_delegated_public_subdomains.*.name_servers,
      aws_route53_zone.id_delegated_public_subdomains.*.name_servers,
      aws_route53_zone.undelegated_public_subdomains.*.name_servers,
    )}"
}
