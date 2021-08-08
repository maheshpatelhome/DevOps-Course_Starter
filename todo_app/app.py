from flask import Flask, render_template, send_from_directory, request, redirect
from oauthlib import oauth2
from todo_app.data.session_items  import add_item, get_item, save_item
from todo_app.todo_view_model import ToDoViewModel
from todo_app.mongo import Mongo
from datetime import date, timedelta
from flask_login import LoginManager, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
from todo_app.user import User
import requests
import os


def create_app():
    app = Flask(__name__)

    client_id=os.getenv('GITHUB_CLIENT_ID')
    client_secret=os.getenv('GITHUB_SECRET')
    app.secret_key=os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthenticated():
        print("unauthorized_handler")
        client = WebApplicationClient(client_id) 
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize')
        return redirect(uri)    
        
    @login_manager.user_loader
    def load_user(user_id):
        return  User(user_id)
    

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
        mongo = Mongo()
        to_do_list = mongo.get_todo_items() 
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday)
        if (len(to_do_view_model.done_items) < 5):
            return render_template('index.html', view_model=to_do_view_model, show_all=True)
        else:
            return render_template('index.html', view_model=to_do_view_model, show_all=False)
            
    @app.route('/', methods=['POST'])
    @login_required
    def add_to_do_item():
        mongo = Mongo()
        mongo.add_item(request.form['todoTitle'])
        return redirect("/")

    @app.route('/doing_item/<card_id>')
    @login_required
    def doing_item(card_id):
        mongo = Mongo()
        mongo.move_to_doing(card_id)
        return redirect("/")

    @app.route('/todo_item/<card_id>')
    @login_required
    def todo_item(card_id):
        mongo = Mongo()
        mongo.move_to_todo(card_id)
        
        return redirect("/")

    @app.route('/done_item/<card_id>')
    @login_required
    def done_item(card_id):
        mongo = Mongo()
        mongo.move_to_done(card_id)
        
        return redirect("/")

    @app.route('/show_all')
    @login_required
    def show_all():
        mongo = Mongo()
        to_do_list = mongo.get_todo_items()
          
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday)
        to_do_view_model.show_all_done = True
        return render_template('index.html', view_model=to_do_view_model, show_all=True)

    @app.route('/show_recent')
    @login_required
    def show_recent():
        mongo = Mongo()
        to_do_list = mongo.get_todo_items()
          
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday)
        to_do_view_model.show_all_done = False
        return render_template('index.html', view_model=to_do_view_model, show_all=False)
    
    if __name__ == '__main__':
        app.run()

    return app