FROM python:3.8 as base

# copy across pyproject.toml and poetry.lock so the dependencies can be installed
RUN mkdir /app
COPY ./poetry.lock /app
COPY ./pyproject.toml /app

#install poetry
RUN pip3 install poetry
WORKDIR /app

#install poetry dependencies from pyprojecy.toml
RUN poetry install

### PRODUCTION ###
#set up the prooduction cntainer to run with gunicorn
FROM base as production

#copy code
COPY . /app

# gunicorn command to run when starting up the container
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:8000 'todo_app.app:create_app()'

# expose port 8000 as this is where gunicorn runs by default
EXPOSE 8000/tcp
### END OF PRODUCTION ###


### DEVELOPMENT ###
FROM base as development

# flask command to run when starting up the container
ENTRYPOINT poetry run flask run --host 0.0.0.0

# expose port 5000 for FLASK
EXPOSE 5000/tcp
### END OF DEVELOPMENT ###