# create-cert-dns

Creates a Let's Encrypt TLS certificate for the specified domain using the DNS challenge. It stores the certificates on the ~/data/certificates

# Arguments
| Name                      | Value Type | Description
|---------------------------| --------   | ---------- 
|`domain`                   | String       | The certificate's primary domain that the certificate will be recognized for.
|`server_url`               | String     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`aws_key `                 | String     | AWS key to authenticate
|`aws_secret `              | String     | AWS key to authenticate
|`zone`                     | String     | Route53 hosted zone
|`region`                   | Integer    | AWS region - e.g. eu-west-1
|`server_urls`               | map(string)     | Registration server URL to use. Valid values are "staging" and "production". Defaults to "production".
|`reg_email`                | Integer    | Email address to register the certificate
|`phishing_server_ip`       | Integer    | IP address of the host to add the certificate

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
