from datetime import datetime

class TrelloCard:

    def __init__(self, list_name, card_id, card_name, last_modified): 
        self.status=list_name
        self.id=card_id
        self.title=card_name
        self.last_modified = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ").date()