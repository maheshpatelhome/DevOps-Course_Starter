import requests
import os 
from dotenv import load_dotenv
from todo_app.trello_card import TrelloCard

class Trello:

    def __init__(self): 
        load_dotenv()
        self.trello_key=os.getenv('API_KEY')
        self.trello_token=os.getenv('API_TOKEN')
        self.board_name=os.getenv('BOARD_NAME')
        self.memberName=os.getenv('MEMBERS_NAME')
        self.to_do_list_name=os.getenv("TO_DO_LIST_NAME")
        self.done_list_name=os.getenv("DONE_LIST_NAME")

    def get_todo_items(self):
        todo_items=[]
        board_id=self.get_board_id()
        trelloLists=self.get_lists_for_board(board_id)
        for key in trelloLists: 
            cards = self.get_cards_for_list(key, trelloLists[key])
            for card_key in cards:
                todo_items.append(cards[card_key]) 
        return todo_items
        
    def add_key_and_token(self, url):   
        return url + "key=" + self.trello_key + "&token=" + self.trello_token

    def get_board_id(self):
        boards_url = self.add_key_and_token("https://api.trello.com/1/members/" + self.memberName + "/boards?")
        request = requests.get(boards_url)
        response = request.json()
        
        for item in response:
            if (item["name"] == self.board_name):
                return item["id"]
        
        #need to raise an error if it returns zero as board cant be found
        return 0
    
    def get_lists_for_board(self, board_id):
        lists = {}
        lists_url = self.add_key_and_token("https://api.trello.com/1/boards/" + board_id + "/lists?")
        request = requests.get(lists_url)
        response = request.json()
        for item in response:
            if (item["closed"] == False):
                lists[item["id"]] = item["name"]

        return lists

    def get_cards_for_list(self, list_id, list_name):
        cards = {}
        cards_for_list_url = self.add_key_and_token("https://api.trello.com/1/lists/" + list_id + "/cards?") 
        request = requests.get(cards_for_list_url)
        response = request.json()
        for item in response:
            card = TrelloCard(list_name, list_id, item["id"], item["name"])
            cards[item["id"]]=card
        
        return cards
    
    def add_item(self, title):
        # need to check title doesnt have any dodgy code
        board_id=self.get_board_id()
        trelloLists=self.get_lists_for_board(board_id)
        for list_id in trelloLists:
            if (trelloLists[list_id] == self.to_do_list_name):
                add_item_url = self.add_key_and_token("https://api.trello.com/1/cards?idList=" + list_id + "&name=" + title + "&")
                requests.post(add_item_url)
        return
    
    def move_list(self, card_id, mark_as_done):
        target_list_id = ""
        board_id=self.get_board_id()
        trelloLists=self.get_lists_for_board(board_id)
        for list_id in trelloLists:
            if (mark_as_done):
                if (trelloLists[list_id] == self.done_list_name):
                    target_list_id = list_id
            else:
                if (trelloLists[list_id] == self.to_do_list_name):
                    target_list_id = list_id
        if (target_list_id != ""):
            move_to_different_list_url = self.add_key_and_token("https://api.trello.com/1/cards/" + card_id + "?idList=" + target_list_id + "&")
            requests.put(move_to_different_list_url)
        return