# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.



This application is dependent on Trello, an account for that will need to be set up
Environment variables will need to be setup for:
API_KEY
API_TOKEN
BOARD_NAME
TO_DO_LIST_ID
DONE_LIST_ID
DOING_LIST_ID


To run the tests run the following commands from the directory where the code has ben checked out to
poetry run pytest todo_app\tests_e2e
poetry run pytest todo_app\tests  



To run the app in a VM via Vagrant use the "vagrant up" command, this will launch a VM with all the dependencies installed and the application can be accessed on http://localhost:5000



To build this app for Docker use for production use:
docker build --target production --tag todo-app:prod .

To build this app for Docker use for development use:
docker build --target development --tag todo-app:dev .

To run the docker container for production use:
docker run -p 9000:8000 --env-file .env todo-app:prod
the application will be available by browsing to http://localhost:9000

To run the docker container for development use:
docker run --mount src="$pwd",target=/app,type=bind -p 9000:5000 --env-file .env todo-app:dev
the application will be available by browsing to http://localhost:9000