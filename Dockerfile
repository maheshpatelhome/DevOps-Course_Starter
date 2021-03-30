FROM python:3.8 as base

#install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

# copy across pyproject.toml and poetry.lock so the dependencies can be installed
RUN mkdir /app
COPY ./poetry.lock /app
COPY ./pyproject.toml /app
WORKDIR /app


### PRODUCTION ###
#set up the prooduction cntainer to run with gunicorn
FROM base as production

#install poetry dependencies from pyprojecy.toml without the dev dependences
RUN poetry install --no-dev

#copy code
COPY . /app

# gunicorn command to run when starting up the container
ENTRYPOINT ["poetry", "run", "gunicorn", "-b",  "0.0.0.0:8000", "todo_app.app:create_app()"]

# expose port 8000 
EXPOSE 8000
### END OF PRODUCTION ###


### DEVELOPMENT ###
FROM base as development

#install poetry dependencies from pyprojecy.toml without the dev dependences
RUN poetry install

# flask command to run when starting up the container
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

# expose port 5000 for FLASK
EXPOSE 5000
### END OF DEVELOPMENT ###