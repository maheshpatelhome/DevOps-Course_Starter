from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id): 
        self.id = id 

    @property
    def role(self):
        if (self.id == 'maheshpatelhome'):
            return "WRITER"
        else:
            return "READER"