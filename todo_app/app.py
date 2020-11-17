
from flask import Flask, render_template, send_from_directory, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items  import add_item, get_item, save_item
from todo_app.trello import Trello
from todo_app.trello_card import TrelloCard

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    trello = Trello()
    to_do_list = trello.get_todo_items() 
    return render_template('index.html', items=to_do_list)

@app.route('/', methods=['POST'])
def add_to_do_item():
    trello = Trello()
    trello.add_item(request.form['todoTitle'])
    return redirect("/")

@app.route('/completed', methods=['POST'])
def mark_item_as_completed():
    #item = get_item(request.form["itemId"])
    #item["status"] = "Completed"
    #save_item(item)
    trello = Trello()
    trello.mark_item_as_done(request.form["itemId"])
    return redirect("/")

if __name__ == '__main__':
    app.run()
