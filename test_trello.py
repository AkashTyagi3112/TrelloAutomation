import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
EMAIL = os.getenv("TRELLO_EMAIL")   
PASSWORD = os.getenv("TRELLO_PASSWORD")

def create_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def wait_for(driver, timeout, locator):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def test_trello_workflow():
    driver = create_driver()
    wait = WebDriverWait(driver, 30)
    driver.get("https://trello.com/login")
    wait_for(driver, 10, (By.XPATH, "//input[@id = 'username-uid1']")).send_keys(EMAIL)
    driver.find_element(By.ID, "login-submit").click()
    time.sleep(2)
    wait_for(driver, 10, (By.XPATH, "//input[@id = 'password']")).send_keys(PASSWORD)
    driver.find_element(By.ID, "login-submit").click()

    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Back to home"]')))
    driver.find_element(By.XPATH, "//p[text() = 'Create']").click()
    driver.find_element(By.XPATH, "//span[text() = 'Create board']").click()

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    board_name = f"QA Scrum Board - AT - {timestamp}"
    driver.find_element(By.XPATH, "//div[text()='Board title']/../input").send_keys(board_name)
    driver.find_element(By.XPATH, "//button[text()='Create']").click()
    wait.until(EC.title_contains(board_name))
    driver.find_element(By.XPATH, "//button[@type='submit']/../../textarea").send_keys('To Do')
    driver.find_element(By.XPATH, "//button[text() = 'Add list']").click()
    driver.find_element(By.XPATH, "//button[@type='submit']/../../textarea").send_keys('In Progress')
    driver.find_element(By.XPATH, "//button[text() = 'Add list']").click()
    driver.find_element(By.XPATH, "//button[@type='submit']/../../textarea").send_keys('Done')
    driver.find_element(By.XPATH, "//button[text() = 'Add list']").click()

#Add Card to lists
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Add a card'])[1]"))).click()
    textarea = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Enter a title or paste a link']")))
    textarea.send_keys("Task_Usecase1")

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Add a card'])[1]"))).click()
    textarea = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Enter a title or paste a link']")))
    textarea.send_keys("Task_Usecase2")

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Add a card'])[2]"))).click()
    textarea = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Enter a title or paste a link']")))
    textarea.send_keys("Task_Usecase3")
    
#Selecting Labels
    driver.find_element(By.XPATH, "(//a[@data-testid='card-name'])[1]").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Labels']"))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-color='green']"))).click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close popover']").click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close dialog']").click()

    driver.find_element(By.XPATH, "(//a[@data-testid='card-name'])[2]").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Labels']"))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-color='yellow']"))).click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close popover']").click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close dialog']").click()

    driver.find_element(By.XPATH, "(//a[@data-testid='card-name'])[3]").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Labels']"))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-color='orange']"))).click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close popover']").click()
    driver.find_element(By.XPATH, "//button[@aria-label='Close dialog']").click()

#Add attachment
    driver.find_element(By.XPATH, "(//a[@data-testid='card-name'])[1]").click() 
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Attachment']"))).click() 
    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Choose a file']/../input")))
    file_path = os.path.abspath("Sample_File.pdf")
    file_input.send_keys(file_path)
    driver.find_element(By.XPATH, "//button[@aria-label='Close dialog']").click()

#Move a card
    source = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[@data-testid='card-name'])[1]")))
    target = wait.until(EC.presence_of_element_located((By.XPATH, "(//h2[@data-testid='list-name'])[2]")))
    actions = ActionChains(driver)
    actions.drag_and_drop(source, target).perform()
    moved = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[@data-testid='card-name'])[2]")))
    destination = wait.until(EC.presence_of_element_located((By.XPATH, "(//h2[@data-testid='list-name'])[3]")))
    actions.drag_and_drop(moved,destination).perform()
    
# Run the script
test_trello_workflow()