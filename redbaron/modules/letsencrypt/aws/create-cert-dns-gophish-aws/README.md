# create-cert-dns

Creates a Let's Encrypt TLS certificate for the specified domain using the DNS challenge. It stores the certificates on the ~/data/certificates

# Example

```hcl
module "create_certs" {
  source = "./modules/letsencrypt/create-cert-dns"

  domains = ["domain.com"]

  subject_alternative_names = {
    "domain.com" = ["www2.domain.com"]
  }
}

#Digital Ocean:
module "create_certs" {
   source = "./modules/letsencrypt/create-cert-dns"
   provider ="digitalocean"
   count = 1
   domains = ["${var.domain[0]}"]
   do_token ="${var.do_token}"
   # subject_alternative_names = {
   #   "${var.domain}" = []
   # }
}
```
# Arguments
| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domains`                  | Yes      | List       | The certificate's primary domain that the certificate will be recognized for.
|`subject_alternative_names`| No       | Map        | The certificate's subject alternative domains that this certificate will also be recognized for.
|`count`                    | No       | Integer    | Number of certificates to create. Defaults to 1.
|`provider_name`            | No       | String     | Provider to use for the DNS challenge. Defaults to "route53".
|`do_token`                 | Yes      | String     | Digital Ocean Token
|`server_url`               | No       | String     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`reg_email`                | No       | String     | Email to use for certificate registration. Defaults to "nobody@example.com"
|`key_type`                 | No       | Integer    | The key type for the certificate's private key. Defaults to 4096.





# Arguments Before Modification

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domains`                  | Yes      | List       | The certificate's primary domain that the certificate will be recognized for.
|`subject_alternative_names`| Yes      | Map        | The certificate's subject alternative domains that this certificate will also be recognized for.
|`count`                    | No       | Integer    | Number of certificates to create. Defaults to 1.
|`provider`                 | No       | String     | Provider to use for the DNS challenge. Defaults to "route53".
|`server_url`               | No       | String     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`reg_email`                | No       | String     | Email to use for certificate registration. Defaults to "nobody@example.com"
|`key_type`                 | No       | Integer    | The key type for the certificate's private key. Defaults to 4096.

# Outputs

| Name                         | Value Type | Description
|----------------------------- | ---------- | -----------
|`certificate_domain`          | String     | 
|`certificate_url`             | String     |
|`certificate_pem`             | String     |
|`certificate_private_key_pem` | String     | 
|`certificate_issuer_pem`      | String     | 
