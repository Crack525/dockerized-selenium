import os
import pytest
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DriverManager:
    """Class to manage the Selenium WebDriver."""
    
    def __init__(self):
        self.driver = None
    

    def setup_driver(self):
        """Set up the WebDriver with mobile emulation options."""
        logger.debug("Setting up the WebDriver")

        # Define custom device metrics (width, height, pixel ratio)
        device_metrics = {
            "width": 412,  # 412 Screen width in pixels
            "height": 914,  # 914 Screen height in pixels
            "pixelRatio": 2.0  # Pixel density (e.g., 2.0 for high-resolution screens)
            }
    
        # Define the user agent for the device
        user_agent = "Mozilla/5.0 (Linux; Android 13; Samsung Galaxy A51/71) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    
        # Set up the Chrome options with mobile emulation
        mobile_emulation = {
        "deviceMetrics": device_metrics,
        "userAgent": user_agent
        }
        
        
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        

        # Set the path to the Chrome binary installed in Docker
        chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"
        
        chrome_service = ChromeService(executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver")
        
        # Initiate selenium driver
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
        

    def quit_driver(self):
        """Quit the WebDriver."""
        if self.driver:
            logger.debug("Quitting the WebDriver")
            self.driver.quit()




@pytest.fixture(scope="module")
def driver():
    """Fixture to set up and tear down the WebDriver."""
    driver_manager = DriverManager()
    
    try:
        driver_manager.setup_driver()
        yield driver_manager.driver
    except Exception as e:
        logger.error(f"Failed to create driver: {str(e)}")
        raise
    finally:
        driver_manager.quit_driver()



@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    """Method called before executing each scenario."""
    logger.info(f"Before Scenario: {scenario.name}")




@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request, feature, scenario):
    """Method called after executing each scenario."""
    logger.info(f"After Scenario: {scenario.name}")

    # Access the existing DriverManager instance from the request
    if hasattr(request.instance, 'driver_manager'):
        request.instance.driver_manager.quit_driver()




@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Method called after executing each step."""
    driver = request.getfixturevalue("driver")  # Accessing the WebDriver from fixtures
    take_screenshot(driver, scenario, step)



def take_screenshot(driver, scenario, step):
    """Capture a screenshot after each step and save with a timestamp."""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    # Define screenshot filename based on scenario name and step name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_name = f"screenshots/{scenario.name.replace(' ', '_')}_{step.name.replace(' ', '_')}_{timestamp}.png"
    
    # Take the screenshot
    driver.save_screenshot(screenshot_name)
    logger.info(f"Screenshot taken for step '{step.name}' in scenario '{scenario.name}': {screenshot_name}")


