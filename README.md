Steps to setup project:
1. `git clone` repository to your local machine
2. `pip install -r requirements.txt` to install all needed dependencies
3. Create `.env` file in main folder of the project and use information from `.env.example` to fill it with needed data
4. Then you need to `cd app` and write `python runserver.py` to run application
5. In case you need to run tests you can go back to first folder like `cd ..` and write `python -m pytest` to run it



Steps to run docker container:
1. Create docker image `docker build -t <your docker image name> .`
2. To run docker container use `docker run -d --name <your docker container name> -p 80:80 <your docker image name>`
3. To run tests inside docker you can use `docker exec -it <your docker container name> python -m pytest`