class TrelloCard:

    def __init__(self, list_name, list_id, card_id, card_name): 
        self.status=list_name
        self.list_id=list_id
        self.id=card_id
        self.title=card_name