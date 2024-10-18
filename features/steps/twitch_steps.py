from datetime import datetime
import time
import logging
from pytest_bdd import scenarios, given, when, then
from conftest import driver  # Relative import
from selenium.webdriver.common.by import By
from features.utility.popup_handler_steps import PopupHandler  # Import the utility class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


# Define the scenarios from the feature file
scenarios('../twitch.feature')
logging.basicConfig(level=logging.INFO)




# Step 1
@given('the user is on the Twitch mobile website')
def step_given_user_on_twitch(driver):
    driver.get("https://m.twitch.tv/")
    popup_handler = PopupHandler(driver)
    popup_handler.accept_cookies()


# Step 2
@then('the user click on search icon')
def step_user_click_action(driver):
    wait = WebDriverWait(driver, 20)
    # Using the XPath selector
    search_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Search']")))
    search_icon.click()
    time.sleep(2)


# Step 3
@then('the user enters StarCraft II')
def step_user_enters_action(driver):
    wait = WebDriverWait(driver, 20)
    max_attempts = 2
    
    for attempt in range(max_attempts):
        try:
            # Locate the search input box
            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-a-target='tw-input']")))
            
            # Clear the input field before sending keys (in case there's existing text)
            search_input.clear()
            search_input.send_keys("StarCraft II")
            
            # Wait for the search results to appear
            wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'starcraft ii - stream')]")))
            
            # If we reach this point, the search was successful
            print(f"Search successful on attempt {attempt + 1}")
            return
        
        except TimeoutException:
            if attempt < max_attempts - 1:
                print(f"Search attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)  # Wait a bit before retrying
            else:
                print("All search attempts failed")
                raise  # Re-raise the exception if all attempts fail
    
    # If we've exhausted all attempts without success
    raise Exception("Failed to see 'starcraft ii - stream' in search results after multiple attempts")  



# Step 4
@then('the user scrolls 2 times')
def step_user_enters_action(driver):
    # Define the number of scrolls
    scroll_count = 2
    scroll_distance = 10000  # Increase scroll distance for deeper scrolling

    for i in range(scroll_count):
        # Scroll down the page by a larger amount
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        logging.info(f"Scrolled down {i + 1} time(s) by {scroll_distance} pixels.")



# Step 5
@then('the user selects starcraft ii - stream')
def step_user_enters_action(driver):
    
    wait = WebDriverWait(driver, 20)
    
    # Wait for the search item to appear
    wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'starcraft ii - stream')]")))
    search_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'starcraft ii - stream')]")))
    search_item.click()
    time.sleep(2)    


    
# Step 6
@then('on the streamer page wait until all is load')
def step_user_waits(driver):
    wait = WebDriverWait(driver, 20)
    # Wait for the search item to appear
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@role='presentation']//a[@data-index='0']//div[contains(@class, 'ScTitle-sc-iekec1-3') and text()='Top']")))
    time.sleep(5)
           
