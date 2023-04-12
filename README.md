## About the project

Service for employee knowledge control

This service will be useful for companies that need to control the knowledge of their employees, test results are recorded in a database, after which the analysis of the received data can be performed and some actions taken against employees.

## Features

-   Created a basic FastAPI project structure, and wraped it in a Docker image;
-   Implemented connection to Postgres and Redis. Run both databases with docker-compose;
-   Implemented authentication for users. JWT tokens - regular and using Auth0 - optional;
-   Implemented quiz functionality, cache responses in Redis for 48 hours, and store results in Postgres;
-   Created a script for checking the date of the last testing for all users by sending a notification to the mail;
-   Covered functionality with tests;

Steps to setup project:
1. `git clone` repository to your local machine
2. `pip install -r requirements.txt` to install all needed dependencies
3. Create `.env` file in main folder of the project and use information from `.env.example` to fill it with needed data



Steps to run docker container:
1. User use docker compose up --build to run all the containers
1. To run docker container use `docker run -d --name <your docker container name> -p 80:80 <your docker image name>`
2. To run tests inside docker you can use `docker exec -it <your docker container name> python -m pytest -s tests`



Steps to create and apply migrations:
1. Command to create migration `docker-compose run --rm <name of docker-compose service> alembic revision --autogenerate -m "<your message>"`
2. To apply migration to database `docker-compose run --rm web alembic upgrade head`


To inspect redis keys:
1. `docker-compose exec redis redis-cli`
2. keys *
3. inspect testing redis keys `docker-compose exec redis redis-cli -h redis -p <port> -n 1`
