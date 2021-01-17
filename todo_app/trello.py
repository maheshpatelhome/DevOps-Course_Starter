import requests
import os 
from dotenv import load_dotenv
from todo_app.trello_card import TrelloCard

class Trello:

    def __init__(self): 
        self.trello_key=os.getenv('API_KEY')
        self.trello_token=os.getenv('API_TOKEN')
        self.board_name=os.getenv('BOARD_NAME')
        self.to_do_list_id=os.getenv("TO_DO_LIST_ID")
        self.done_list_id=os.getenv("DONE_LIST_ID")
        self.doing_list_id=os.getenv("DOING_LIST_ID")
    
    def get_todo_items(self):
        todo_items=[]
        board_id=self.get_board_id(self.board_name)
        trelloLists=self.get_lists_for_board(board_id)
        for key in trelloLists: 
            cards = self.get_cards_for_list(key, trelloLists[key])
            for card_key in cards:
                todo_items.append(cards[card_key]) 
        return todo_items
        
    def add_key_and_token(self, url):   
        return f"{url}key={self.trello_key}&token={self.trello_token}"

    def get_board_id(self, board_name):
        boards_url = self.add_key_and_token("https://api.trello.com/1/members/me/boards?")
        request = requests.get(boards_url)
        response = request.json()
        
        for item in response:
            if (item["name"] == board_name):
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
            card = TrelloCard(list_name, list_id, item["id"], item["name"], item["dateLastActivity"])
            cards[item["id"]]=card
        
        return cards
    
    def add_item(self, title):
        add_item_url = self.add_key_and_token("https://api.trello.com/1/cards?")
        requests.post(add_item_url, params={"name" : title, "idList": self.to_do_list_id})
        return

    def move_to_doing(self, card_id):
        self.move__to_list(card_id, self.doing_list_id)
        return
    
    def move_to_done(self, card_id):
        self.move__to_list(card_id, self.done_list_id)
        return
    
    def move_to_todo(self, card_id):
        self.move__to_list(card_id, self.to_do_list_id)
        return

    def move__to_list(self, card_id, list_id):
        move_to_different_list_url = self.add_key_and_token("https://api.trello.com/1/cards/" + card_id + "?idList=" + list_id + "&")
        requests.put(move_to_different_list_url)
        return

    