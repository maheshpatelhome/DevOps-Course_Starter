from flask import Flask, render_template, send_from_directory, request, redirect
from todo_app.data.session_items  import add_item, get_item, save_item
from todo_app.todo_view_model import ToDoViewModel
from todo_app.mongo import Mongo
from datetime import date, timedelta

def create_app():
    app = Flask(__name__)

    @app.route('/')
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
    def add_to_do_item():
        mongo = Mongo()
        mongo.add_item(request.form['todoTitle'])
        return redirect("/")

    @app.route('/doing_item/<card_id>')
    def doing_item(card_id):
        mongo = Mongo()
        mongo.move_to_doing(card_id)
        return redirect("/")

    @app.route('/todo_item/<card_id>')
    def todo_item(card_id):
        mongo = Mongo()
        mongo.move_to_todo(card_id)
        
        return redirect("/")

    @app.route('/done_item/<card_id>')
    def done_item(card_id):
        mongo = Mongo()
        mongo.move_to_done(card_id)
        
        return redirect("/")

    @app.route('/show_all')
    def show_all():
        mongo = Mongo()
        to_do_list = mongo.get_todo_items()
          
        yesterday = date.today() - timedelta(days = 1) 

        to_do_view_model = ToDoViewModel(to_do_list, yesterday)
        to_do_view_model.show_all_done = True
        return render_template('index.html', view_model=to_do_view_model, show_all=True)

    @app.route('/show_recent')
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