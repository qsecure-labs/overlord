# dns-rdir

Creates a DNS Redirector server in AWS. SSH keys for each instance will be outputted to the ssh_keys folder. The redirector points to an internal server of choice using the autossh tool.

# Arguments

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`subnet_id`                | String     | Subnet ID to create instance in.
|`vpc_id`                   | String     | ID of VPC to create instance in.
|`redirect_to`              | List(string)       | List of IPs to redirect DNS traffic to.
|`counter`                  | Integer    | Number of instances to launch. Defaults to 1.
|`instance_type`            | String     | Instance type to launch. Defaults to "t2.medium"
|`amis`                     | Map(string)       | The ami which is to be installed (according to the distro specified)

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created instances.
