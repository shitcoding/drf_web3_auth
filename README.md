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
- `/api/events/` - get the paginated list of smart contract events parsed to Django database
- `/api/message/<str:eth_address>/` - get one-time message to sign for web3/JWT authorization
- `/api/auth/web3/` - get JWT refresh/access tokens using signed message

---
## Tests

- testing endpoint generating one-time message to sign
- testing signature verification
- testing JWT authorization and accessing restricted endpoint

1. Spin up the services and create env file
```bash
make env && make up
```
2. Run: `make test-api`

