import pytest
import requests
from todo_app import app
from todo_app.todo_card import TodoCard
from todo_app.mongo import Mongo
from flask import request
from datetime import datetime
from dotenv import find_dotenv, load_dotenv


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
 
    # Create the new app.
    test_app = app.create_app()
    
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client    

class MockListOfCardsResponse(object):
    def _init__ (self):
        self.status_code = 200

@pytest.fixture
def mock_get_requests_2(monkeypatch):    
    def get_mocked_request_get(arg1):
        return MockListOfCardsResponse

    def get_mocked_to_do_list(arg1):
        to_do_items = []
        card1 = TodoCard("Doing", 1, "hide button when done", datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        card2 = TodoCard("Done",  2, "test the app", datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        card3 = TodoCard("To Do", 2, "add ability to restart", datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        to_do_items.append(card1)
        to_do_items.append(card2)
        to_do_items.append(card3)
        return to_do_items

    monkeypatch.setattr(Mongo, "get_todo_items", get_mocked_to_do_list)
    monkeypatch.setattr(requests, "get",  get_mocked_request_get)

def test_index_page_2(mock_get_requests_2, client):
    response = client.get('/')
    assert response.status ==  "200 OK"
    assert str(response.data).find("hide button when done") > -1
    assert str(response.data).find("test the app") > -1
    assert str(response.data).find("add ability to restart") > -1
    