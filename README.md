# EVS Notifications System
Nobody wants their aircon to switch off in the middle of the night when their credit runs out.  

The EVS notification system scrapes your credit balance daily. When your balance falls below a preset threshold, the system notifies you via Telegram bot.

## Architecture
Click [here](assets/architecture.jpg) for an image of the system architecture.  

All operations involving data is done through individual corresponding APIs.

### Components
* Postgres database
* Vue website for dashboard analytics
* Telegram bot

### APIs
* CRUD operations for database
* GET operations only for dashboard
* Endpoint for fetching balance via web scraping
* Endpoint for sending one-time messages via Telegram bot

### Daily-run services
* Scrape all user balances and add to database
* Retrieve all users to notify and send notifications

## Pre-requisites
1. Python 3.6+
1. Either:
	* Postgres 9.5
	* Docker
1. NodeJS

## Deployment
### Python
The following components use Python:
* APIs (Flask)
* Telegram bot (python-telegram-bot)
* Daily-run services

All Python-based components have a `requirements.txt` file in their corresponding folder.

### Vue dashboard
There is a corresponding README in the `dashboard` folder. A static site is bundled using Webpack and used for hosting.

### Postgres
The database is run from a Docker container. To get a database up and running on your local machine:
```
docker pull postgres:9.5
docker run --rm -d \
    --name pg-docker \
    -e POSTGRES_USER=ubuntu \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=evs \
    -p 5432:5432 \
    -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data \
    postgres:9.5
```

Afterwards, to connect to the database:
```
PGPASSWORD=docker psql -h localhost -U postgres -d evs
```

For first-time setup, run `\i create_tables.sql` to define database schema.