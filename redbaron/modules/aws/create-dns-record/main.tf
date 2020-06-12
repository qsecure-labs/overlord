terraform {
  required_version = ">= 0.11.0"
}

# Add a record to the domain
resource "aws_route53_record" "record" {
  count   = var.counter
  zone_id = var.zone
  name    = element(keys(var.records), count.index)
  type    = var.type
  ttl     = var.ttl
  # TF-UPGRADE-TODO: In Terraform v0.10 and earlier, it was sometimes necessary to
  # force an interpolation expression to be interpreted as a list by wrapping it
  # in an extra set of list brackets. That form was supported for compatibility in
  # v0.11, but is no longer supported in Terraform v0.12.
  #
  # If the expression in the following list itself returns a list, remove the
  # brackets to avoid interpretation as a list of lists. If the expression
  # returns a single list item then leave it as-is and remove this TODO comment.
  records = var.records[element(keys(var.records), count.index)]
}

