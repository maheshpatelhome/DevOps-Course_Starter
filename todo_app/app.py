
from flask import Flask, render_template, send_from_directory, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items  import get_items, add_item
from todo_app.trello_config import TrelloConfig


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    config = TrelloConfig()
    print ('running app ' + config.trello_key + ' ' + config.trello_token) 
    to_do_list = get_items()
    return render_template('index.html', items=to_do_list)

@app.route('/', methods=['POST'])
def add_to_do_item():
    add_item(request.form['todoTitle'])
    return redirect("/")

if __name__ == '__main__':
    app.run()
