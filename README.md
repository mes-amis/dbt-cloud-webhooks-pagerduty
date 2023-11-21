# PagerDuty Lambda

## Overview

https://docs.getdbt.com/guides/serverless-pagerduty?step=1

## Requirements

Python 3.11+

- [dbtc](https://dbtc.dpguthrie.com) - Unofficial python interface to dbt Cloud APIs
- [FastAPI](https://fastapi.tiangolo.com) - Modern, fast, web framework for building APIs with Python 3.11+
- [requests](https://requests.readthedocs.io/en/latest/) - Elegant and simple HTTP library for Python, built for human beings

## Getting Started

Clone this repo

```bash
git clone https://github.com/mes-amis/dbt-cloud-webhooks-pagerduty.git
```

### Secrets

The following secrets need to be configured to your runtime environment for your application to work properly.

- `DBT_CLOUD_AUTH_TOKEN` - his is the secret key that's shown after initailly creating your webhook subscription in dbt Cloud
- `DBT_CLOUD_SERVICE_TOKEN` - Generate a [service token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens#generating-service-account-tokens) in dbt Cloud. Ensure that it has at least the `Metadata Only` permission as we will be making requests against the Metadata API.
- `PD_ROUTING_KEY` - Use the integration key for your integration (will be used as `routing_key`). More info [here](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started)
