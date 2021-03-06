import os
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import requests
import pytest
from todo_app.trello import Trello
from todo_app import app
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.by import By

@pytest.fixture()
def driver():
    with webdriver.Firefox() as driver:
        yield driver

@pytest.fixture()
def test_app():
    
    #file_path = find_dotenv('.env.test.e2e')
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    os.environ['API_KEY'] = os.getenv('API_KEY')
    os.environ['API_TOKEN'] = os.getenv('API_TOKEN')
    
    board_id = create_trello_board("TestBoard")
    os.environ['TRELLO_BOARD_ID'] = board_id
    os.environ['BOARD_NAME'] = "TestBoard"
    os.environ['TO_DO_LIST_ID'] = get_list_id_for_board(board_id, "TO DO")
    os.environ['DONE_LIST_ID'] = get_list_id_for_board(board_id, "DONE")
    os.environ['DOING_LIST_ID'] = get_list_id_for_board(board_id, "DOING")
    
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board(board_name):
    trello = Trello()
    create_board_url = trello.add_key_and_token("https://api.trello.com/1/boards?name=" + board_name + "&")
    http_response = requests.post(create_board_url)
    response = http_response.json()
    return response["id"]

def get_list_id_for_board(board_id, list_name):
    trello = Trello()
    lists_url = trello.add_key_and_token("https://api.trello.com/1/boards/" + board_id + "/lists?")
    http_response = requests.get(lists_url)
    response = http_response.json()
    for item in response:
        if list_name.upper() == item["name"].upper():
            list_id = item["id"]
    return list_id

def delete_trello_board(board_id):
    trello = Trello()
    delete_board_url = trello.add_key_and_token("https://api.trello.com/1/boards/" + board_id + "?")
    requests.delete(delete_board_url)
    return

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

def test_can_create_new_to_do_item(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    to_do_list_table_cell = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in todo table and none in the doing and done
    assert len(to_do_list_table_rows) == 1
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 0
    #make sure the todo table row has a value and the text is "New Selenium Test Item"
    assert to_do_list_table_cell.text == new_card_name
    
def test_can_create_new_to_do_item_and_start_it(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    doing_button = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[2]/a[text()='Doing']")
    doing_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='doing-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_cell = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in doing table and none in the todo and done
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 1
    assert len(done_list_table_rows) == 0
    #make sure the doing table row has a value and the text is "New Selenium Test Item"
    assert doing_list_table_cell.text == new_card_name

def test_can_create_new_to_do_item_and_complete_it(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    done_button = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[2]/a[text()='Done']")
    done_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_cell = driver.find_element_by_xpath("//table[@id='done-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in done table and none in the todo and doing
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 1
    #make sure the done table row has a value and the text is "New Selenium Test Item"
    assert done_list_table_cell.text == new_card_name

def test_can_create_new_to_do_item_start_it_complete_it(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    to_do_list_table_cell = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in todo table and none in the doing and done
    assert len(to_do_list_table_rows) == 1
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 0
    #make sure the todo table row has a value and the text is "New Selenium Test Item"
    assert to_do_list_table_cell.text == new_card_name
    
    doing_button = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[2]/a[text()='Doing']")
    doing_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='doing-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_cell = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in doing table and none in the todo and done
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 1
    assert len(done_list_table_rows) == 0
    #make sure the doing table row has a value and the text is "New Selenium Test Item"
    assert doing_list_table_cell.text == new_card_name

    done_button = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[2]/a[text()='Done']")
    done_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_cell = driver.find_element_by_xpath("//table[@id='done-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in done table and none in the todo and doing
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 1
    #make sure the done table row has a value and the text is "New Selenium Test Item"
    assert done_list_table_cell.text == new_card_name


def test_can_create_new_to_do_item_start_it_and_complete_it(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    to_do_list_table_cell = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in todo table and none in the doing and done
    assert len(to_do_list_table_rows) == 1
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 0
    #make sure the todo table row has a value and the text is "New Selenium Test Item"
    assert to_do_list_table_cell.text == new_card_name
    
    doing_button = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[2]/a[text()='Doing']")
    doing_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='doing-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_cell = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in doing table and none in the todo and done
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 1
    assert len(done_list_table_rows) == 0
    #make sure the doing table row has a value and the text is "New Selenium Test Item"
    assert doing_list_table_cell.text == new_card_name

    done_button = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[2]/a[text()='Done']")
    done_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_cell = driver.find_element_by_xpath("//table[@id='done-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in done table and none in the todo and doing
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 1
    #make sure the done table row has a value and the text is "New Selenium Test Item"
    assert done_list_table_cell.text == new_card_name


def test_can_create_new_to_do_item_start_it_complete_it_and_restart_it(driver, test_app):
    new_card_name = "New Selenium Test Item"
    driver.get('http://localhost:5000/')
    new_to_do_textbox = driver.find_element_by_name("todoTitle")
    new_to_do_textbox.send_keys(new_card_name)
    save_button = driver.find_element_by_id("save_new")
    save_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='to-do-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    to_do_list_table_cell = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in todo table and none in the doing and done
    assert len(to_do_list_table_rows) == 1
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 0
    #make sure the todo table row has a value and the text is "New Selenium Test Item"
    assert to_do_list_table_cell.text == new_card_name
    
    doing_button = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody/tr[1]/td[2]/a[text()='Doing']")
    doing_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='doing-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_cell = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in doing table and none in the todo and done
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 1
    assert len(done_list_table_rows) == 0
    #make sure the doing table row has a value and the text is "New Selenium Test Item"
    assert doing_list_table_cell.text == new_card_name

    done_button = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[2]/a[text()='Done']")
    done_button.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='done-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_cell = driver.find_element_by_xpath("//table[@id='done-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in done table and none in the todo and doing
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 0
    assert len(done_list_table_rows) == 1
    #make sure the done table row has a value and the text is "New Selenium Test Item"
    assert done_list_table_cell.text == new_card_name

    doing_button_in_done_table = driver.find_element_by_xpath("//table[@id='done-table']/tbody/tr[1]/td[2]/a[text()='Doing']")
    doing_button_in_done_table.click()

    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='doing-table']/tbody/tr[1]"))
    WebDriverWait(driver, 60).until(element_present)

    to_do_list_table_rows = driver.find_element_by_xpath("//table[@id='to-do-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_rows = driver.find_element_by_xpath("//table[@id='doing-table']/tbody").find_elements_by_tag_name("tr")
    done_list_table_rows = driver.find_element_by_xpath("//table[@id='done-table']/tbody").find_elements_by_tag_name("tr")
    doing_list_table_cell = driver.find_element_by_xpath("//table[@id='doing-table']/tbody/tr[1]/td[1]")

    #make sure there is one row in doing table and none in the todo and done
    assert len(to_do_list_table_rows) == 0
    assert len(doing_list_table_rows) == 1
    assert len(done_list_table_rows) == 0
    #make sure the doing table row has a value and the text is "New Selenium Test Item"
    assert doing_list_table_cell.text == new_card_name
