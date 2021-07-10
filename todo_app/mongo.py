import os
from bson.objectid import ObjectId
import pymongo 
from dotenv import load_dotenv
from todo_app.trello_card import TrelloCard
from datetime import datetime

class Mongo:
    def __init__(self): 
        self.user_name=os.getenv('USER_NAME')
        self.password=os.getenv('PASSWORD')
        self.mongo_url=os.getenv('MONGO_URL')
        self.default_database=os.getenv('DEFAULT_DATABASE')
        self.board_name=os.getenv('BOARD_NAME')
        self.connection_string = "mongodb+srv://" + self.user_name + ":" + self.password + "@" + self.mongo_url + "/" + self.default_database + "?w=majority"
        
    def getClient(self):
        return pymongo.MongoClient(self.connection_string)

    def get_databases(self):
        client = self.getClient()
        databases = client.list_database_names()
        for item in databases:
            print (item)

    def get_cards_for_board(self):
        client = self.getClient()
        to_do_app_database = client["To_Do_App"]
        to_do_items_collection = to_do_app_database['ToDoItems']
        cards= {}
        for item in to_do_items_collection.find({"board_name" : self.board_name}):
            formatted_date = item["date_last_activity"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            card = TrelloCard(item["list_name"], item["_id"], item["name"], formatted_date)
            cards[item["_id"]]=card        
        return cards

    def get_todo_items(self):
        todo_items=[]
        cards = self.get_cards_for_board()
        for card_key in cards:
            todo_items.append(cards[card_key])
        return todo_items

    def add_item(self, title):
        client = self.getClient()
        to_do_app_database = client["To_Do_App"]
        to_do_items_collection = to_do_app_database['ToDoItems']

        item_to_add = {
            "board_name":self.board_name,
            "list_name":"To Do",
            "name":title,
            "date_last_activity": datetime.today()
        }
        to_do_items_collection.insert_one(item_to_add)
        return

    def move_to_list(self, card_id, list_name):
        client = self.getClient()
        to_do_app_database = client["To_Do_App"]
        to_do_items_collection = to_do_app_database['ToDoItems']

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

    def delete_date_for_board(self, board_name):
        client = self.getClient()
        to_do_app_database = client["To_Do_App"]
        to_do_items_collection = to_do_app_database['ToDoItems']
        to_do_items_collection.delete_many({"board_name" : board_name})
        return
