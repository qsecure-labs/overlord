# ansible

Runs an ansible playbook on a specific resource

# Arguments

| Name                      | Required | Value Type   | Description
|---------------------------| -------- | ------------ | -----------
|`playbook`                 | Yes      | String       | Playbook to run
|`ip`                       | Yes      | String       | Host to run playbook on
|`user`                     | Yes      | String       | User to authenticate as over SSH
|`arguments`                | No       | List(string) | Additional Ansible arguments
|`envs`                     | No       | List(string) | Environment variable to pass to Ansible


# Outputs

| Name                      | Value Type   | Description
|---------------------------| ------------ | -----------
|`arguments`                | List(string) | Additional Ansible arguments
|`envs`                     | List(string) | Environment variable to pass to Ansible
