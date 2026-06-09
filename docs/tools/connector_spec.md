# Connector Spec

Connectors are source adapters for the research agent.

The first repo version does not implement live external connectors. It defines the contract so future work can add APIs without changing the research workflow.

## Connector Fields

- `id`: stable connector ID.
- `name`: human-readable source name.
- `source_type`: web, api, manual, local, browser.
- `requires_api_key`: true or false.
- `env_var`: environment variable for credential, if needed.
- `rate_limit`: known limit or unknown.
- `cost_risk`: none, low, medium, high.
- `supports_claims`: claim types the connector can support.
- `outputs`: expected output artifacts.
- `fallbacks`: lower-quality source options.
- `notes`: limitations.

## Claim Types

- `pricing`
- `packaging`
- `usage_limit`
- `retention`
- `revenue`
- `cost`
- `distribution`
- `strategy`
- `user_behavior`
- `competition`
- `app_rank`
- `download_estimate`
- `traffic_estimate`
- `funding`
- `shutdown`
- `acquisition`

## Connector Quality Rules

- Official source connectors beat third-party connectors for pricing and packaging.
- Third-party app intelligence can support rankings and estimates, but must be labeled as estimates.
- News connectors can discover events, but official confirmation should be collected when possible.
- Manual evidence must include collection date and collector note.

