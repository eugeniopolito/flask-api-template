# Docker multi container for Python Flask APIs development

This Docker multi container can ease the process of configuring a Flask App from scratch. <br>
It includes everything you need to start developing your Flask APIs:

- Python 3.7
- Pipenv
- Flask
- Flask RESTful
- Flask JWT Extended
- Flask SQLAlchemy
- Flask Migrate 
- Flask Marshmallow
- Marshmallow SQLAlchemy
- Marshmallow
- MariaDB database engine (as a Docker service) 

There are four APIs built for you, so you immediately can manage users registration, login, logout and refresh the JWT token without writing any code:

- /v1/register
- /v1/login
- /v1/logout
- /v1/refresh

## Credits

This project is based on the code from this repository:

https://github.com/tecladocode/rest-api-sections

which is a companion code of a great Flask course (more info here: https://blog.tecladocode.com).

## Requirements

The only requirement to execute the image is a working <b>Docker engine</b>
and a terminal program where you can execute the `docker-compose` command.

## Installation steps

- You need to make a copy of `.env.example` to `.env` file in the root project and set the `JWT_SECRET_KEY` as you prefer. <br>
- In order to build the container for the first time, open your terminal and execute the following command:

```
docker-compose build
```

> As you can see in `docker-compose.yml`, there are two services for the container: one for the Flask App - the  `web` 
service - and one another for the MariaDB image -  `db` service. <br> 

- To run both the services, just type in your console:

```
docker-compose up
```

## Project structure 

- `models` contains the models app, managed by *SQLAlchemy*
- `schemas` contains the *Marshmallow* mapping schemas
- `resources` contains the *Flask-RESTful* resources
- `templates` contains the *Jinja2* templates
- `tests` contains integration and system tests
- `lookup_tables` contains useful lookup tables. The `messages.py` contains the message codes sent by the APIs to the client.
- `migrations` contains the `Flask-Migrate` and `Alembic` scripts and files for Database auto migrations 

> All migrations are run by the `start.sh`
automatically at the container startup, so: if you add a new class model than you need to restart the server in order to run migrations 


## Test APIs 

Now the server is up and running, you can test the application in your browser at this address: `http://127.0.0.1:5000/`. <br> 
You should see a message with installed Flask version.<br>
You can test the APIs with the test suite `run_all_tests.py`. <br>
Be sure to start the container before you run them, because system tests require a running server. <br> 
Enjoy!
