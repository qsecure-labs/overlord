# create-cert-phishing

# Dependencies ERRORS ( on development does not work as intended)
Creates a Let's Encrypt TLS certificate for the specified domain using the DNS challenge on the Phishing Server and restarts the service on HTTPS.

# Arguments
| Name                      | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domain`                  | String       | The certificate's primary domain that the certificate will be recognized for.
|`counter`                  | Integer    | Number of certificates to create. Defaults to 1.
|`phishing_server_ip`       | List(string)    | IP address of the host to add the certificate
|`email`                | String    | Email address to register the certificate|`do_token`                 | Yes      | String     | Digital Ocean Token
