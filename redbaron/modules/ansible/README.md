# ansible

Runs an ansible playbook on a specific resource

# Arguments

| Name                      | Value Type   | Description
|---------------------------| ------------ | -----------
|`playbook`                 | String       | Playbook to run
|`ip`                       | String       | Host to run playbook on
|`user`                     | String       | User to authenticate as over SSH
|`arguments`                | List(string) | Additional Ansible arguments
|`envs`                     | List(string) | Environment variable to pass to Ansible


# Outputs

| Name                      | Value Type   | Description
|---------------------------| ------------ | -----------
|`arguments`                | List(string) | Additional Ansible arguments
|`envs`                     | List(string) | Environment variable to pass to Ansible
