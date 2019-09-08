# email-server

Creates a droplet in DigitalOcean to be used as a mail server. SSH keys for each droplet will be outputted to the ssh_keys folder.

# Example

```hcl
module "email_server" {
  source = "./modules/digitalocean/mail-server"
}
```

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`counter`                  | No       | Integer    | Number of droplets to launch. Defaults to `1`.
|`size`                     | No       | String     | Droplet size to launch. Defaults to `1gb with 25 GB disk`.
|`regions`                  | No       | List       | Regions to create Droplet(s) in. Defaults to `LON1`. Accepted values are NYC1/2/3, SFO1/2, AMS2/3, SGP1, LON1, FRA1, TOR1, BLR1.

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created droplets.
