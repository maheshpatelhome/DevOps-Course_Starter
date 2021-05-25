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

#install poetry dependencies from pyprojecy.toml 
RUN poetry install

# flask command to run when starting up the container
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

# expose port 5000 for FLASK
EXPOSE 5000
### END OF DEVELOPMENT ###

### TEST ###
FROM base as test

#install poetry dependencies from pyprojecy.toml
RUN poetry install

#update package list, otherwise google chrome wont install
RUN apt-get update
 
# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
apt-get install ./chrome.deb -y &&\
rm ./chrome.deb

#Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
echo "Installing chromium webdriver version ${LATEST}" &&\
curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
apt-get install unzip -y &&\
unzip ./chromedriver_linux64.zip

#copy code
COPY . /app 

# command to run tests
ENTRYPOINT ["poetry", "run", "pytest"]

### END OF TEST ###