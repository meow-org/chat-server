# Chat server
Server side of the chat. Application created using the flask framework and postgres database.
Before starting work, install docker and docker-compose
## Run server
* Run command docker-compose up --build -d 

Server starting on http://0.0.0.0:5000 address.

## Environment file
To set up the project, place the env_file file containing the following fields:
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=USE_YOUR_PASSWORD
* POSTGRES_DB=flaskapp_db
* APP_SECRET_KEY=SUPER_SECRET_KEY
* MAIL_DEFAULT_SENDER=YOUR_EMAIL_ADDRESS
* MAIL_SERVER=smtp.googlemail.com
* MAIL_PORT=587
* MAIL_USE_TLS=True
* MAIL_USERNAME=YOUR NAME
* MAIL_PASSWORD=XXXXXXXXfgbfbf
* FLASK_ENV=development
## Migration commands
For migration to the server used [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) library.



