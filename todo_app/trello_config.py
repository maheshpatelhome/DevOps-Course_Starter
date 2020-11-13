import os 
from dotenv import load_dotenv

class TrelloConfig:

    def __init__(self): 
        load_dotenv()
        self.trello_key=os.getenv('API_KEY')
        self.trello_token=os.getenv('API_TOKEN')