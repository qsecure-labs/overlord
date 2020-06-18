# create-hosted-zone

Redirects the nameservers from Godaddy to another provider (AWS, DigitalOcean)

# Arguments

| Name                      | Required | Value Type   | Description
|---------------------------| -------- | ------------ | -----------
|`domain`                   | Yes      | String       | The domain to create a hosted zone for.
|`nameservers`              | Yes      | List(string) | The nameservers to be used for the specified domain.
