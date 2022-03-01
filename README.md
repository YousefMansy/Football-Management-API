## Football Management API

## Instructions

### Running Locally
1. `pip install poetry`
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. Run the DB migrations via poetry `poetry run ./prestart.sh` (only required once)
4. Run the FastAPI server via poetry `poetry run ./run_local.sh`
5. Create a postgres Database to use
6. Add your db connection string as `SQLALCHEMY_DATABASE_URI` in `core/config.py`
7. Open http://localhost:8001/docs for the API Swagger documentation

###  Running using Docker

1. Run `docker-compose -f docker-compose.local.yml up -d`