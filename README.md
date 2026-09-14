# Work Orders Service

Small FastAPI service created for the TripleTen AI Systems Engineering pre-cohort warm-up.

## Features

- POST `/work-orders` creates a work order
- GET `/work-orders/{id}` returns a work order
- PostgreSQL database
- Invalid input returns HTTP 400
- Unknown work order IDs return HTTP 404
- Automated round-trip test with pytest

## Requirements

- Python 3
- Docker
- Git

## Start PostgreSQL

```bash
docker run \
  --name wo-db \
  -e POSTGRES_PASSWORD=dev \
  -p 5433:5432 \
  -d postgres:16
```

## If the container already exists:

docker start wo-db

## Create the Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run the service
uvicorn main:app --reload

## Open Swagger in a browser:

http://127.0.0.1:8000/docs

## Example request

POST /work-orders

{
  "title": "Repair conveyor sensor",
  "status": "open"
}

## Run the test

## Make sure PostgreSQL is running, then run:

pytest -v
