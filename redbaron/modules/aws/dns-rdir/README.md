# dns-rdir

Creates a DNS Redirector server in AWS. SSH keys for each instance will be outputted to the ssh_keys folder.

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`subnet_id`                | Yes      | String     | Subnet ID to create instance in.
|`vpc_id`                   | Yes      | String     | ID of VPC to create instance in.
|`redirect_to`              | Yes      | List       | List of IPs to redirect DNS traffic to.
|`counter`                  | No       | Integer    | Number of instances to launch. Defaults to 1.
|`instance_type`            | No       | String     | Instance type to launch. Defaults to "t2.medium"
|`amis`                     | Yes      | List       | The ami which is to be installed (according to the distro specified)

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created instances.
