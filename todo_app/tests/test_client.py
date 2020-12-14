from dotenv import find_dotenv, load_dotenv
import pytest
import requests
import pathlib
from todo_app import app
from todo_app.trello import Trello
from todo_app.trello_card import TrelloCard
from flask import request, json
import os

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

class MockResponse(object):
    def _init__ (self):
        self.status_code = 200

    def json(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        datafile = directory + '\cards.json'
        file = pathlib.Path(datafile)
    
        with file.open() as json_data:
            contents = json.load(json_data)

        return contents

@pytest.fixture
def mock_get_requests_2(monkeypatch):
    def get_mocked_board(arg1): 
        return "TestToDoBoard"
    
    def get_mocked_lists_on_board(arg1, arg2): 
        lists = {}
        lists["1"] = "TO DO"
        return lists
    
    def get_mocked_request_get(arg1):
        return MockResponse()

    monkeypatch.setattr(Trello, "get_board_id", get_mocked_board)
    monkeypatch.setattr(Trello, "get_lists_for_board", get_mocked_lists_on_board)
    monkeypatch.setattr(requests, "get",  get_mocked_request_get)

def test_index_page_2(mock_get_requests_2, client):
    response = client.get('/')
    assert response.status ==  "200 OK"
    assert str(response.data).find("hide button when done") > -1
    assert str(response.data).find("test the app") > -1
    assert str(response.data).find("add ability to restart") > -1
    