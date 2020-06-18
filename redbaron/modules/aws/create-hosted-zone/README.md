# create-hosted-zone

Creates a hosted zone for a domain in AWS Route53.

# Arguments

| Name                      | Required | Value Type | Description
|---------------------------| -------- | ---------- | -----------
|`public_hosted_zones`      | Yes      | Map        | The domain to create a hosted zone for.
|`tags`                     | Yes      | List       | Choose who ise the owner of the hosted Zones, environment etc.
|`comment`                  | Yes      | String     | Comments to be added in the Route53


# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`zone_id`                  | String     | The created hosted zone ID.
|`name_servers`             | Array      | The name servers for this zone.
