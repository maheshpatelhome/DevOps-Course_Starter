from flask import Flask, render_template, send_from_directory, request, redirect, flash
from oauthlib import oauth2
from todo_app.data.session_items  import add_item, get_item, save_item
from todo_app.todo_view_model import ToDoViewModel
from todo_app.mongo import Mongo
from datetime import date, timedelta
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from todo_app.user import User
from loggly.handlers import HTTPSHandler
from logging import Formatter

import requests
import os
import logging

def create_app():
    app = Flask(__name__)

    #logging.basicConfig(filename='ToDoApp.log', level=logging.INFO, format='%(asctime)s - %(module)s - %(message)s')
    logging.basicConfig(
        format='%(asctime)s - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler("ToDoApp.log"),
            logging.StreamHandler()
        ])
    logger = logging.getLogger(__name__)
    logging.getLogger().setLevel(os.getenv('LOG_LEVEL'))
    
    loggly_token = os.getenv('LOGGLY_TOKEN')
    if loggly_token is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{loggly_token}/tag/todo-app')
        handler.setFormatter( Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    app.logger.addHandler(handler)

    client_id=os.getenv('GITHUB_CLIENT_ID')
    client_secret=os.getenv('GITHUB_SECRET')
    app.secret_key=os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(client_id) 
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize')
        return redirect(uri)    
        
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    
    @app.route('/login/callback', methods=['GET', 'POST'])
    def callback():
        code = request.values['code']
        client = WebApplicationClient(client_id) 
        url, headers, body = client.prepare_token_request('https://github.com/login/oauth/access_token', code=code)
        git_access_key = requests.post(url, headers=headers, data=body, auth=(client_id, client_secret))
        git_json = client.parse_request_body_response(git_access_key.text)
        git_user_request = client.add_token("https://api.github.com/user")
        git_user = requests.get(git_user_request[0], headers=git_user_request[1]).json()
        git_login = User(git_user['login'])
        login_user(git_login)
        return redirect('/')

    @app.route('/')
    @login_required
    def index():
        logger.info("Getting ToDo data")
        mongo = Mongo()
        to_do_list = mongo.get_todo_items() 
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday, user_has_write_permissions())
        if (len(to_do_view_model.done_items) < 5):
            return render_template('index.html', view_model=to_do_view_model, show_all=True)
        else:
            return render_template('index.html', view_model=to_do_view_model, show_all=False)
            
    @app.route('/', methods=['POST'])
    @login_required
    def add_to_do_item():
        if (user_has_write_permissions() == False):
            flash("You do not have permissions to do this action")
            logger.warn("User does not have rights to add ToDo data")
        else:
            logger.info("Adding ToDo Item %s", request.form['todoTitle'])
            mongo = Mongo()
            mongo.add_item(request.form['todoTitle'])
        return redirect("/")

    @app.route('/doing_item/<card_id>')
    @login_required
    def doing_item(card_id):
        if (user_has_write_permissions() == False):
            flash("You do not have permissions to do this action")
            logger.warn("User does not have rights to move ToDo item to Doing list")
        else:
            logger.info("Moving Card ID %s to Doing list", card_id)
            mongo = Mongo()
            mongo.move_to_doing(card_id)
        return redirect("/")

    @app.route('/todo_item/<card_id>')
    @login_required
    def todo_item(card_id):
        if (user_has_write_permissions() == False):
            flash("You do not have permissions to do this action")
            logger.warn("User does not have rights to move ToDo data to ToDo list")
        else:
            logger.info("Moving Card ID %s to ToDo list", card_id)
            mongo = Mongo()
            mongo.move_to_todo(card_id)
        
        return redirect("/")

    @app.route('/done_item/<card_id>')
    @login_required
    def done_item(card_id):
        if (user_has_write_permissions() == False):
            flash("You do not have permissions to do this action")
            logger.warn("User does not have rights to move ToDo data to Done list")
        else:
            logger.info("Moving Card ID %s to Done list", card_id)
            mongo = Mongo()
            mongo.move_to_done(card_id)
        
        return redirect("/")

    @app.route('/show_all')
    @login_required
    def show_all():
        mongo = Mongo()
        to_do_list = mongo.get_todo_items()
          
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday, user_has_write_permissions())
        to_do_view_model.show_all_done = True
        return render_template('index.html', view_model=to_do_view_model, show_all=True)

    @app.route('/show_recent')
    @login_required
    def show_recent():
        mongo = Mongo()
        to_do_list = mongo.get_todo_items()
          
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday, user_has_write_permissions())
        to_do_view_model.show_all_done = False
        return render_template('index.html', view_model=to_do_view_model, show_all=False)
    
    def user_has_write_permissions():
        return current_user.role == "WRITER"

    if __name__ == '__main__':
        app.run()

    return app