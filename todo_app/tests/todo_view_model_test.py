from todo_app.todo_view_model import ToDoViewModel
from todo_app.trello_card  import TrelloCard
import pytest
from datetime import date, datetime, timedelta

@pytest.fixture
def items_setup():
    items = [
        TrelloCard("To Do", 1, "To Do Item 1", "2020-12-01T00:00:00.000Z"),
        TrelloCard("To Do", 2, "To Do Item 2", "2020-12-01T00:00:00.000Z" ),
        TrelloCard("To Do", 3, "To Do Item 3", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Doing", 4, "Doing Item 4", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Doing", 5, "Doing Item 5", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Done", 6, "Done Item 6", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Random, should only be returned by items", 7, "Random Item 7", "2020-12-01T00:00:00.000Z")
    ]
    return items

@pytest.fixture
def empty_items_setup():
    items = []
    return items

@pytest.fixture
def done_items_with_dates_setup():
    items = [
        TrelloCard("To Do", 1, "To Do Item 1", "2020-12-01T00:00:00.000Z"),
        TrelloCard("To Do", 2, "To Do Item 2", "2020-12-01T00:00:00.000Z"),
        TrelloCard("To Do", 3, "To Do Item 3", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Doing", 4, "Doing Item 4", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Doing", 5, "Doing Item 5", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Done", 6, "Done Item 6", "2020-12-01T00:00:00.000Z"),
        TrelloCard("Done", 7, "Done Item 7", "2020-12-02T00:00:00.000Z"),
        TrelloCard("Done", 8, "Done Item 8", "2020-12-02T00:00:00.000Z"),
        TrelloCard("Done", 9, "Done Item 9", "2020-12-03T00:00:00.000Z"),
        TrelloCard("Done", 10, "Done Item 10", "2020-12-03T00:00:00.000Z"),
        TrelloCard("Done", 11, "Done Item 11", "2020-12-03T00:00:00.000Z"),
        TrelloCard("Done", 12, "Done Item 12", "2020-12-02T00:00:00.000Z")
    ]
    return items

def test_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup, date.today())
    assert len(sut.items) == 7
    assert sut.items == items_setup

def test_to_do_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup, date.today())
    result = sut.to_do_items
    assert len(result) == 3
    assert result[0] == items_setup[0]
    assert result[1] == items_setup[1]
    assert result[2] == items_setup[2]

def test_doing_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup, date.today())
    result = sut.doing_items
    assert len(result) == 2
    assert result[0] == items_setup[3]
    assert result[1] == items_setup[4]

def test_done_items_returns_correct_data_when(items_setup):
    sut = ToDoViewModel(items_setup, date.today())
    result = sut.done_items
    assert len(result) == 1
    assert result[0] == items_setup[5]

def test_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup, date.today())
    assert len(sut.items) == 0
    
def test_to_do_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup, date.today())
    result = sut.to_do_items
    assert len(result) == 0
    
def test_doing_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup, date.today())
    result = sut.doing_items
    assert len(result) == 0
    
def test_done_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup, date.today())
    result = sut.done_items
    assert len(result) == 0
    
def test_recent_done_items_returns_correct_data(done_items_with_dates_setup):
    todays_date_for_test = "2020-12-03T00:00:00.000Z"
    yesterdays_date_for_test = datetime.strptime(todays_date_for_test, "%Y-%m-%dT%H:%M:%S.%fZ").date() - timedelta(days = 1)
    sut = ToDoViewModel(done_items_with_dates_setup, yesterdays_date_for_test)
    result = sut.recent_done_items
    assert len(result) == 3
    assert result[0] == done_items_with_dates_setup[8]
    assert result[1] == done_items_with_dates_setup[9]
    assert result[2] == done_items_with_dates_setup[10]

def test_older_done_items_returns_correct_data(done_items_with_dates_setup):
    todays_date_for_test = "2020-12-03T00:00:00.000Z"
    yesterdays_date_for_test = datetime.strptime(todays_date_for_test, "%Y-%m-%dT%H:%M:%S.%fZ").date() - timedelta(days = 1)
    sut = ToDoViewModel(done_items_with_dates_setup, yesterdays_date_for_test)
    result = sut.older_done_items
    assert len(result) == 4
    assert result[0] == done_items_with_dates_setup[5]
    assert result[1] == done_items_with_dates_setup[6]
    assert result[2] == done_items_with_dates_setup[7]
    assert result[3] == done_items_with_dates_setup[11]