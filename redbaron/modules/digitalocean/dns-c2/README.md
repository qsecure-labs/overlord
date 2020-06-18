# dns-c2

Creates a DNS C2 server in DigitalOcean. SSH keys for each droplet will be outputted to the ssh_keys folder.

# Arguments

| Name                      | Required | Value Type   | Description
|---------------------------| -------- | ------------ | -----------
|`install`                  | No       | List         | Scripts to run on droplet creation. Defaults to "./scripts/core_deps.sh".
|`counter`                  | Yes      | Integer      | Number of droplets to launch. Defaults to 1.
|`distro`                   | Yes      | Integer      | Number of droplets to launch. Defaults to 1.
|`size`                     | No       | String       | Droplet size to launch. Defaults to `1gb with 25 GB disk`.
|`regions`                  | Yes      | List(string) | Regions to create Droplet(s) in. Defaults to `NYC1`. Accepted values are NYC1/2/3, SFO1/2, AMS2/3, SGP1, LON1, FRA1, TOR1, BLR1.
|`available_regions`        | No       | Map(string)  | Regions to choose from in the regions variable

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created droplets.