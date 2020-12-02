
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

@app.route('/doing_item/<card_id>')
def doing_item(card_id):
    trello = Trello()
    trello.move_to_doing(card_id)
    return redirect("/")

@app.route('/todo_item/<card_id>')
def todo_item(card_id):
    trello = Trello()
    trello.move_to_todo(card_id)
    return redirect("/")

@app.route('/done_item/<card_id>')
def done_item(card_id):
    trello = Trello()
    trello.move_to_done(card_id)
    return redirect("/")

@app.route('/sort_status/<in_order>')
def sort_status(in_order):
    print("sort status " + in_order)
    trello = Trello()
    to_do_list = trello.get_todo_items()
    if in_order == "asc":
        sorted_to_do_list = sorted(to_do_list, key=lambda card: card.status)
    else:
        sorted_to_do_list = sorted(to_do_list, key=lambda card: card.status, reverse=True) 
    print("first item " + sorted_to_do_list[0].title)
    return render_template('index.html', items=sorted_to_do_list)
    #return redirect("/")


if __name__ == '__main__':
    app.run()
