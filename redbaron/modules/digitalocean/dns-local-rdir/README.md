# dns-rdir

Creates a DNS Redirector droplet in DigitalOcean. SSH keys for each droplet will be outputted to the ssh_keys folder. The redirector points to an internal server of choice using the autossh tool.

# Arguments

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`redirect_to`              | List(string)       | List of IPs to redirect DNS traffic to.
|`counter`                  | Integer    | Number of droplets to launch. Defaults to `1`.
|`size`                     | String     | Droplet size to launch. Defaults to `1gb with 25 GB disk`.
|`regions`                  | List(string)       | Regions to create Droplet(s) in. Defaults to `NYC1`. Accepted values are NYC1/2/3, SFO1/2, AMS2/3, SGP1, LON1, FRA1, TOR1, BLR1.
|`available_regions`        | Map(string)  | Regions to choose from in the regions variable

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created droplets.