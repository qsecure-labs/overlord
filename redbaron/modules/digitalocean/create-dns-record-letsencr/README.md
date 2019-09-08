# create-dns-record-letsencr

Adds records to a domain using DigitalOcean. Then runs certbot to create a TLS certificate. 
(Created due to dependency issues with the specific module. "letsencrypt/create-cert-phishing" must be fixed)

# Example

```hcl
module "create_root_record" {
  source = "./modules/digitalocean/create-dns-record-letsencr"
  phishing_server_ip = "${module.phishing_server.ips}"
  name  = "@"
  domain = "${var.domain[0]}"
  type = "A"
  records = {
    "${var.domain[0]}" = "${module.http_rdir.ips[0]}"
  }
}
```

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domain`                   | Yes      | String     | The domain to add records to
|`type`                     | Yes      | String     | The record type to add. Valid values are A, AAAA, CAA, CNAME, MX, NAPTR, NS, PTR, SOA, SPF, SRV and TXT.
|`records`                  | Yes      | Map        | A map of records to add. Domains as keys and IPs as values.
|`name`                     | Yes      | String     | Use @ to create the record at the root of the domain or enter a hostname to create it elsewhere. A records are for IPv4 addresses only and tell a request where your domain should direct to.
|`phishing_server_ip`       | Yes      | String     | The IP of the phishing server so it could ssh
|`counter`                  | No       | Integer    | DONT USE IT. I will need to modify the script to make it work or DELETE it.
|`ttl`                      | No       | Integer    | The TTL of the record(s). Default value is 300
|`email`                    | No       | String     | Default to fakeemail@a.com 



# Arguments Before 

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`domain`                   | Yes      | String     | The domain to add records to
|`type`                     | Yes      | String     | The record type to add. Valid values are A, AAAA, CAA, CNAME, MX, NAPTR, NS, PTR, SOA, SPF, SRV and TXT.
|`records`                  | Yes      | Map        | A map of records to add. Domains as keys and IPs as values.
|`count`                    | No       | Integer    | Number of records to add. Default value is 1
|`ttl`                      | No       | Integer    | The TTL of the record(s). Default value is 300
# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`records`                  | Map        | Map containing the records added to the domain. Domains as keys and IPs as values.

