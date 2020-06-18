# phishing-server

Creates an instance in AWS to be used as a phishing server (with Gophish installed). SSH keys for each instance will be outputted to the ssh_keys folder.

# Arguments

| Name                      | Required | Value Type   | Description
|---------------------------| -------- | ------------ | -----------
|`subnet_id`                | Yes      | String       | Subnet ID to create instance in.
|`vpc_id`                   | Yes      | String       | ID of VPC to create instance in.
|`counter`                  | No       | Integer      | Number of instances to launch. Defaults to 1.
|`instance_type`            | No       | String       | Instance type to launch. Defaults to "t2.medium"
|`install`                  | No       | List(string) | Scripts to run on instance creation. Defaults to "./scripts/core_deps.sh".
|`amis`                     | Yes      | List         | The ami which is to be installed (according to the distro specified)

# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`ips`                      | List       | IPs of created instances.
