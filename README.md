# Airflow SQLite Docker Compose
![airflow-sqlite-docker](thumbnail.webp "Airflow SQLite Docker")

# Introduction
This repo deploy a development Airflow instance with an SQLite metadata backend using Docker Compose. 

Note: 
* Question 1 - is available in airflow-sqlite folder, with path data/question1

* Question 2 - airflow-sqlite
- Read ClickHouse database
- Load to SQLite

* Question 3 - named question3
- Reads a JSON file.
- Sniffs the schema of the JSON file.
- Dumps the schema output to a specified directory.

### Initial Setup
Run the `init.sh` script to create the supporting folders and `.env` file.
- Make `init.sh` executable: ```chmod +x init.sh```
- Run `init.sh`: ```./init.sh```

### Deploy Airflow with Custom Image
- Update the `docker-compose.yml`. Comment the line `image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.8.0}` and uncomment the line `build: .`. [reference](https://airflow.apache.org/docs/apache-airflow/2.7.0/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file)
- Create `Dockerfile` and `requirements.txt` file. 
- Build custom Docker image: `docker compose build`
- Start docker containers: `docker compose up -d` or `docker compose up --build -d`

### Login to Airflow UI
- Go to `http://localhost:8585`
- Login with the username and password. The default username and password are `airflow` and `airflow`, respectively.
### Configure Connection on Airflow UI
configure clickehouse and sqlite to airflow ui
- Go to the menu directory: Admin > Connections
- Setup clickhouse_conn and sqlite connection

## Commands
- Build custom Airflow Image: `docker compose build`
- Spin Up Docker Containers: `docker compose up -d`
- Stop Docker Containers: `docker compose stop`
- Start stopped Docker Containers: `docker compose start`
- Destroy Docker Containers: `docker compose down --volumes --remove-orphans`

## References
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/2.8.0/howto/docker-compose/index.html)
