# Chat server
Server side of the chat. Application created using the flask framework and postgres database.
Before starting work, install docker and docker-compose
## Run containers
Run command 

```docker-compose up --build -d``` 

2 containers start. The first container with the database, the second with the server

## Environment file
To set up the project, place the env_file file containing the following fields:
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=USE_YOUR_PASSWORD
* POSTGRES_DB=flaskapp_db
* POSTGRES_TEST_DB=test
* APP_SECRET_KEY=SUPER_SECRET_KEY
* MAIL_DEFAULT_SENDER=YOUR_EMAIL_ADDRESS
* MAIL_SERVER=smtp.googlemail.com
* MAIL_PORT=587
* MAIL_USE_TLS=True
* MAIL_USERNAME=YOUR NAME
* MAIL_PASSWORD=XXXXXXXX
* FLASK_ENV=development
* BASE_URL_APP=http://localhost:3000

## Run development server

If you are starting the server for the first time, use the following commands

```docker-compose exec flaskapp python manage.py db upgrade``` - this command create a database

```docker-compose exec flaskapp python manage.py seed``` - create test data

```docker-compose exec flaskapp python manage.py run``` - this command run flask develop server

## Migration commands

```docker-compose exec flaskapp python manage.py db migrate```

Create new migration. Use if you change models.

```docker-compose exec flaskapp python manage.py db upgrade``` - create tables, update tables

```docker-compose exec flaskapp python manage.py db downgrade``` - drop tables

For more info [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) library or use command ```docker-compose exec python manage.py db --help```

## Production 

```docker-compose -f docker-compose.yml -f docker-compose-production.yml up -d```

Start production server using gunicorn. More information [Gunicorn](https://gunicorn.org/)

## Tests

```docker-compose exec python flaskapp manage.py tests all``` - run all tests
```docker-compose exec python flaskapp manage.py db tests report``` - run tests and build coverage report





