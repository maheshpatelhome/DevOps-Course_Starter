from flask_login import UserMixin

class TestUser(UserMixin):
    @property
    def role(self):
        return "WRITER"