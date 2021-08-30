import os
from bson.objectid import ObjectId
import pymongo 
from dotenv import load_dotenv
from todo_app.todo_card import TodoCard
from datetime import datetime

class Mongo:
    def __init__(self): 
        #self.user_name=os.getenv('USER_NAME')
        #self.password=os.getenv('PASSWORD')
        #self.mongo_url=os.getenv('MONGO_URL')
        self.default_database=os.getenv('DEFAULT_DATABASE')
        self.board_name=os.getenv('BOARD_NAME')
        #self.connection_string = "mongodb+srv://" + self.user_name + ":" + self.password + "@" + self.mongo_url + "/" + "?w=majority"
        #self.connection_string = "mongodb://mahesh-todo-app:D0bJ964nvDVTtnr8fb893A33KFQcuzcf2c4oRwXqITwEZSCU173K60yMmCeLjCONZdgqOayUzyD1cKMFun9FFg==@mahesh-todo-app.mongo.cosmos.azure.com:10255/DefautDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@mahesh-todo-app@"
        self.connection_string = os.getenv('COSMOS_CONNECTION_STRING')

    def getToDoCollection(self):
        client = pymongo.MongoClient(self.connection_string)
        to_do_app_database = client[self.default_database]
        to_do_items_collection = to_do_app_database['ToDoItems']
        return to_do_items_collection    

    def get_todo_items(self):
        to_do_items_collection = self.getToDoCollection()
        cards= []
        for item in to_do_items_collection.find({"board_name" : self.board_name}):
            formatted_date = item["date_last_activity"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            card = TodoCard(item["list_name"], item["_id"], item["name"], formatted_date)
            cards.append(card)
        return cards

    def add_item(self, title):
        to_do_items_collection = self.getToDoCollection()
        item_to_add = {
            "board_name":self.board_name,
            "list_name":"To Do",
            "name":title,
            "date_last_activity": datetime.today()
        }
        to_do_items_collection.insert_one(item_to_add)
        return

    def move_to_list(self, card_id, list_name):
        to_do_items_collection = self.getToDoCollection()
        item_to_update = {
            "list_name":list_name,
            "date_last_activity": datetime.today()
        }
        to_do_items_collection.update_one({"_id":ObjectId(card_id)}, {"$set": item_to_update}, upsert=False)
        return

    def move_to_doing(self, card_id):
        self.move_to_list(card_id, "Doing")
        return
    
    def move_to_done(self, card_id):
        self.move_to_list(card_id, "Done")
        return
    
    def move_to_todo(self, card_id):
        self.move_to_list(card_id, "To Do")
        return

    def delete_data_for_board(self, board_name):
        to_do_items_collection = self.getToDoCollection()
        to_do_items_collection.delete_many({"board_name" : board_name})
        to_do_items_collection.drop()
        return
