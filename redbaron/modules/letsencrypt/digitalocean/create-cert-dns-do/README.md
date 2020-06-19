# create-cert-dns

Creates a Let's Encrypt TLS certificate for the specified domain using the DNS challenge. It stores the certificates on the ~/data/certificates

# Arguments
| Name                      | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`provider_name`            | String     | Provider to use for the DNS challenge. Defaults to "route53".
|`do_token`                 | String     | Digital Ocean Token
|`domain`                  | String       | The certificate's primary domain that the certificate will be recognized for.
|`server_url`               | String     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`server_urls`               | Map(string)     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`reg_email`                | String     | Email to use for certificate registration. Defaults to "nobody@example.com"


# Outputs

| Name                         | Value Type | Description
|----------------------------- | ---------- | -----------
|`certificate_domain`          | String     | 
|`certificate_url`             | String     |
|`certificate_pem`             | String     |
|`certificate_private_key_pem` | String     | 
|`certificate_issuer_pem`      | String     | 
|`certificate_file_path`      | String     | 
|`certificate_private_key_file_path`      | String     | 
