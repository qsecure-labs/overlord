# create-hosted-zone

Creates a hosted zone for a domain in AWS Route53.

# Arguments

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`public_hosted_zones`      | List(string)        | The domain to create a hosted zone for.
|`delegation_set_name`                     | String       | Create a shared delegation set among specefied hosted zones domains if not empty. (nmutually exclusive to 'delegation_set_id').
|`delegation_set_id`                     | String       | Assign specified hosted zones to a delegation set specified by ID if not empty. (mutually exclusive to 'delegation_set_reference_name').
|`custom_subdomain_ns`                     | List(string)       | Hosted zones for subdomains require nameserver to be specified explicitly. You can use this variable to add a list of custom nameserver IP addresses. If left empty it will be populated by four AWS default nameserver.
|`default_subdomain_ns_ttl`                     | String       | Hosted zones for subdomains require nameserver to be specified explicitly. This sets their default TTL.
|`tags`                     | Map(string)       | The resource tags that should be added to all hosted zone resources.
|`comment`                  | String     | Comments to be added in the Route53


# Outputs

| Name                      | Value Type | Description
|---------------------------| ---------- | -----------
|`zone_id`                  | String     | The created hosted zone ID.
|`name_servers`             | Array      | The name servers for this zone.
