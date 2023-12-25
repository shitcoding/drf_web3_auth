# DRF app with web3 authentication
---
## Usage

1. `make env` to create `.env` file from `.env.example` template
2. Add/change credentials/settings in `.env` file
3. `make up` - launch app (starts all required services: DRF app, Postgres DB, Redis, Celery worker/beat)

After launch:
- `make create-superuser` - to create Django superuser with your credentials
- `make create-test-superuser` - to automatically create test superuser with predefined credentials

---
## Endpoints
`/api/events` - get the paginated list of smart contract events parsed to Django database
