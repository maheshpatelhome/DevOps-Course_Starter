from dotenv import find_dotenv, load_dotenv
import pytest
from todo_app import app
from todo_app.trello import Trello
from todo_app.trello_card import TrelloCard

#from Flask import json


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

@pytest.fixture
def mock_get_requests(monkeypatch):
    def get_mocked_to_do_items(arg):
        mocked_to_do_items = [
            TrelloCard("To Do", 1, 1, "To Do Item 1", "2020-12-01T00:00:00.000Z"),
            TrelloCard("To Do", 1, 2, "To Do Item 2", "2020-12-01T00:00:00.000Z" ),
            TrelloCard("To Do", 1, 3, "To Do Item 3", "2020-12-01T00:00:00.000Z"),
            TrelloCard("Doing", 2, 4, "Doing Item 4", "2020-12-01T00:00:00.000Z"),
            TrelloCard("Doing", 2, 5, "Doing Item 5", "2020-12-01T00:00:00.000Z"),
            TrelloCard("Done", 3, 6, "Done Item 6", "2020-12-01T00:00:00.000Z"),
            TrelloCard("Random, should only be returned by items", 4, 7, "Random Item 7", "2020-12-01T00:00:00.000Z")
        ] 
        return mocked_to_do_items

    monkeypatch.setattr(Trello, "get_todo_items", get_mocked_to_do_items)
    
def test_index_page(mock_get_requests, client):
    response = client.get('/')
    assert response.status ==  "200 OK"
    assert str(response.data).find("To Do Item 1") > -1
    assert str(response.data).find("To Do Item 2") > -1
    assert str(response.data).find("To Do Item 3") > -1
    assert str(response.data).find("Doing Item 4") > -1
    assert str(response.data).find("Doing Item 5") > -1
    assert str(response.data).find("Done Item 6") > -1
    