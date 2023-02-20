Steps to setup project:
1. `git clone` repository to your local machine
2. `pip install -r requirements.txt` to install all needed dependencies
3. Create `.env` file in main folder of the project and use information from `.env.example` to fill it with needed data
4. Then you need to `cd app` and write `uvicorn main:app --reload` to run application
5. In case you need to run tests you can go back to first folder like `cd ..` and write `python -m pytest` to run it