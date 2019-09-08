terraform {
  required_version = ">= 0.11.0"
}

# Add a record to the domain
resource "aws_route53_record" "record" {
  count = "${var.counter}"
  zone_id = "${var.zone}"
  name = "${element(keys(var.records), count.index)}"
  type = "${var.type}"
  ttl = "${var.ttl}"
  records = ["${lookup(var.records, element(keys(var.records), count.index))}"]
}
