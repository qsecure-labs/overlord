# create-hosted-zone

Redirects the nameservers from Godaddy to another provider (AWS, DigitalOcean)

# Example

```hcl
module "redirect_ns"{
  source = "./modules/godaddy/redirect-nameservers"
  domain = "${var.domain[1]}"

  # // specify any custom nameservers for your domain
  nameservers = ["ns1.test.com"]
}

```

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domain`                   | Yes      | String     | The domain to create a hosted zone for.
|`nameservers`              | Yes      | List       | The nameservers to be used for the specified domain.
