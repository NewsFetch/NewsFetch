# API

## Local development

### Installation

To install the API, first clone the repository, and navigate to the `newsfetch-api` directory.

Other installation instructions are the same as for the whole project and can be found [here](../intro.md).

### Usage

To start the API, first activate the virtual environment.

```bash
source venv/bin/activate
```

Then, make a copy of `.env.sample` to `.env`, and start the API.

This will start the API with SQLite database. To use a different database, update the `DATABASE_URL` in `.env` file.
The sample API uses SQLAlchemy, and supports all databases supported by SQLAlchemy.

```bash
uvicorn fast_api.main:app --reload
```

This will start the API on `http://localhost:8000`.

## Ingesting data into the database

To ingest data into the database, run the following command.

```bash
python ingest_data.py
```

This will ingest data from the directory specified in the environment variable
SOURCE_FOLDER to the database via the API. The API endpoint is specified in the
environment variable API_ENDPOINT.

The data being ingested is expected to have the valid format that has been defined in the APIs datamodel.
The datamodel can be found in the file `newsfetch-api/core/db_models.py`.
The wire format of the data is defined in the file `newsfetch-core/api_schemas.py`.

## Docker

### Build 

Run this from the root directory of the project.

```bash
docker build -t newsfetch/newsfetch-api -f ./Dockerfile-sampleapi .
```

### Pull from DockerHub

The image is also available on DockerHub.

```bash
docker pull newsfetch/newsfetch-api
```

### Run

Now the API can be started using the following command.

```bash
docker run -d -p 8000:8000 newsfetch/newsfetch-api
```

## Render Deployment

### Build command
`./render_build.sh`

### Start command
`uvicorn fastapi_main:app --host 0.0.0.0`

