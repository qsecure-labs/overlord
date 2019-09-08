# create-domain

Adds a domain list to Digital Ocean

# Example

```hcl
module "create_domain_name" {
  source = "./modules/digitalocean/create-domain"
  counter = "${length("${var.domain}")}"
  name = "${var.domain}"
}
```

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`name`                     | Yes      | List       | The domain names to add 

# Output
| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`domain_name`              | LIST       | Domain name list
