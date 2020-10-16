from flask import Flask, render_template, send_from_directory, request
from todo_app.flask_config import Config

from todo_app.data.session_items  import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    toDoList = get_items()
    return render_template('index.html', items=toDoList)

@app.route('/', methods=['POST'])
def addToDoItem():
    print('item to add = ' + request.form['todoTitle'])

    add_item(request.form['todoTitle']) 
    toDoList = get_items()
    return render_template('index.html', items=toDoList)


if __name__ == '__main__':
    app.run()
