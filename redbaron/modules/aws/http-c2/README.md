# http-c2

Creates a HTTP C2 server in AWS. SSH keys for each instance will be outputted to the ssh_keys folder.

# Arguments

| Name                      | Value Type   | Description
|---------------------------| ------------ | -----------
|`subnet_id`                | String       | Subnet ID to create instance in.
|`vpc_id`                   | String       | ID of VPC to create instance in.
|`counter`                  | Integer      | Number of instances to launch. Defaults to 1.
|`instance_type`            | String       | Instance type to launch. Defaults to "t2.medium"
|`install`                  | List(string) | Scripts to run on instance creation. Defaults to "./scripts/core_deps.sh".
|`amis`                     | Map(string)  | The ami which is to be installed (according to the distro specified)
|`user`                     | String       | User to be used to login with SSH (different for each distro on AWS)

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created instances.
