# Getting Started

After cloning the repository, you need to make a Python virtual environment for it:

`python3 -m venv geode-db-query`

Then activate the virtual environemnt:

`source geode-db-query/bin/activate`

And install the dependencies:

`pip3 install -r requirements`

# Overview

The code uses Python [Fast API](https://fastapi.tiangolo.com/) for REST API development.
Database access is handled with the [SQLAlchemy)[https://www.sqlalchemy.org/] library.

The main web app code is in `main.py`. 
There are database models in `models.py` -- these are used by SQLAlchemy. Each model corresponds to a database table.
There are some database helper functions in `dby.py` -- these are used by `main.py`.

Each API endpoint, such as `/events`, is defined in `main.py`. These are short functions which 
call a helper function in `db.py` and does some mimimal post-processing of the results.

# Geode REST API Deployment

Currently

1) Install the [Azure CLI tools](https://learn.microsoft.com/en-us/cli/azure/).

2) Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). If you are on a Mac, be sure
to select the version for the right type of chip (Intel vs M1).

3) Ensure Docker Desktop is running.

4) Open a Terminal window and run `az acr login --name  geojsonapi`

    You should see a message: "Login Succeeded" 
    If you do not, then follow the on-screen instructions

5) Edit the code as desired.

6) Package the code as a Docekr iamge. 