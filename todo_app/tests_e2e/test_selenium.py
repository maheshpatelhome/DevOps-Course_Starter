import os
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import pytest
from todo_app import app
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.by import By
from todo_app.mongo import Mongo

@pytest.fixture()
def driver():
    #with webdriver.Firefox() as driver:
    #    yield driver

    # for chromium options https://peter.sh/experiments/chromium-command-line-switches/
    # to stop :ERROR:ssl_client_socket_impl.cc(947)] handshake failed; returned -1, SSL error code 1, net_error -101
    # https://stackoverflow.com/questions/37883759/errorssl-client-socket-openssl-cc1158-handshake-failed-with-chromedriver-chr
    # to stop usb error
    #https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument('--no-sandbox')
    #opts.add_argument('--disable-dev-shm-usage')
    #opts.add_argument('--disable-webgl')
    #opts.add_argument('--disable-gpu')
    #opts.add_argument('--ignore-certificate-errors')
    #opts.add_argument('--ignore-ssl-errors')
    #opts.add_argument('--ignore-certificate-errors-spki-list')

    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver
    
@pytest.fixture()
def test_app():
    
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    os.environ['BOARD_NAME'] = "TestBoard"
    os.environ['DEFAULT_DATABASE'] = "E2ETest"
 
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    delete_test_data("TestBoard")

def delete_test_data(board_name):
    mongo = Mongo()
    mongo.delete_data_for_board(board_name)

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
