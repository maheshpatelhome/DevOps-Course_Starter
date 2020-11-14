
from flask import Flask, render_template, send_from_directory, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items  import get_items, add_item, get_item, save_item
from todo_app.trello_config import TrelloConfig


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    config = TrelloConfig()
    print ('running app ' + config.trello_key + ' ' + config.trello_token) 
    to_do_list = sorted(get_items(), key=lambda item: item["status"], reverse=True)
    return render_template('index.html', items=to_do_list)

@app.route('/', methods=['POST'])
def add_to_do_item():
    add_item(request.form['todoTitle'])
    return redirect("/")

@app.route('/completed', methods=['POST'])
def mark_item_as_completed():
    item = get_item(request.form["itemId"])
    item["status"] = "Completed"
    save_item(item)
    return redirect("/")

if __name__ == '__main__':
    app.run()
