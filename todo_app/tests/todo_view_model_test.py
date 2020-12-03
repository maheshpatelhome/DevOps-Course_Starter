from todo_app.todo_view_model import ToDoViewModel
from todo_app.trello_card  import TrelloCard
import pytest

@pytest.fixture
def items_setup():
    items = []
    item1 = TrelloCard("To Do", 1, 1, "To Do Item 1")
    item2 = TrelloCard("To Do", 1, 2, "To Do Item 2")
    item3 = TrelloCard("To Do", 1, 3, "To Do Item 3")
    item4 = TrelloCard("Doing", 2, 4, "Doing Item 4")
    item5 = TrelloCard("Doing", 2, 5, "Doing Item 5")
    item6 = TrelloCard("Done", 3, 6, "Done Item 6")
    item7 = TrelloCard("Random, should only be returned by items", 4, 7, "Random Item 7")

    items.append(item1)
    items.append(item2)
    items.append(item3)
    items.append(item4)
    items.append(item5)
    items.append(item6)
    items.append(item7)
    return items

@pytest.fixture
def empty_items_setup():
    items = []
    return items

def test_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup)
    assert len(sut.items) == 7
    assert sut.items == items_setup

def test_to_do_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup)
    result = sut.to_do_items
    assert len(result) == 3
    assert result[0] == items_setup[0]
    assert result[1] == items_setup[1]
    assert result[2] == items_setup[2]

def test_doing_items_returns_correct_data(items_setup):
    sut = ToDoViewModel(items_setup)
    result = sut.doing_items
    assert len(result) == 2
    assert result[0] == items_setup[3]
    assert result[1] == items_setup[4]

def test_done_items_returns_correct_data_when(items_setup):
    sut = ToDoViewModel(items_setup)
    result = sut.done_items
    assert len(result) == 1
    assert result[0] == items_setup[5]

def test_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup)
    assert len(sut.items) == 0
    
def test_to_do_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup)
    result = sut.to_do_items
    assert len(result) == 0
    
def test_doing_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup)
    result = sut.doing_items
    assert len(result) == 0
    
def test_done_items_returns_correct_data_when_items_is_empty(empty_items_setup):
    sut = ToDoViewModel(empty_items_setup)
    result = sut.done_items
    assert len(result) == 0
    