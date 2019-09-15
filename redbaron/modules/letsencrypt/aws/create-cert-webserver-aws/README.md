# create-cert-phishing

# Dependencies ERRORS ( on development does not work as intended)
Creates a Let's Encrypt TLS certificate for the specified domain using the DNS challenge on the Phishing Server and restarts the service on HTTPS.

# Example

```hcl
# module "lets_encrypt" {
  source = "./modules/letsencrypt/create-cert-phishing"
  # count = 1
  # domains = "${var.domain}"
  domain = "${module.create_root_record.domain}"
  phishing_server_ip = "${module.phishing_server.ips[0]}"
}

```
# Arguments
| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domains`                  | Yes      | List       | The certificate's primary domain that the certificate will be recognized for.
|`subject_alternative_names`| No       | Map        | The certificate's subject alternative domains that this certificate will also be recognized for.
|`counter`                  | No       | Integer    | Number of certificates to create. Defaults to 1.
|`provider_name`            | No       | String     | Provider to use for the DNS challenge. Defaults to "route53".
|`do_token`                 | Yes      | String     | Digital Ocean Token
|`server_url`               | No       | String     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`reg_email`                | No       | String     | Email to use for certificate registration. Defaults to "nobody@example.com"
|`key_type`                 | No       | Integer    | The key type for the certificate's private key. Defaults to 4096.




# Outputs

| Name                         | Value Type | Description
|----------------------------- | ---------- | -----------
