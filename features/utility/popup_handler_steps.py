import datetime
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

logging.basicConfig(level=logging.INFO)


class PopupHandler:
    def __init__(self, driver):
        self.driver = driver
        
   
    def accept_cookies(self):
        
        wait = WebDriverWait(self.driver, 10)
    
        try:
            # Wait for page load
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(2)
        
            # Try to directly set cookies and trigger acceptance
            result = self.driver.execute_script("""
                // Function to create and set cookies
                function setCookie(name, value, days) {
                    const date = new Date();
                    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                    document.cookie = name + "=" + value + "; expires=" + date.toUTCString() + "; path=/";
                }
            
                // Set common consent cookies
                setCookie("consent-banner", "true", 365);
                setCookie("twitch.gdpr.consent", "true", 365);
            
                // Try multiple methods to remove the banner
                try {
                    // Method 1: Find and trigger the original click handler
                    const acceptButton = document.querySelector('button[data-a-target="consent-banner-accept"]');
                    if (acceptButton) {
                        // Get all click event listeners
                        const handlers = getEventListeners(acceptButton);
                        if (handlers && handlers.click) {
                            handlers.click.forEach(handler => handler.listener.call(acceptButton));
                        }
                    }
                
                    // Method 2: Direct banner removal
                    const banner = document.querySelector('.consent-banner');
                        if (banner) {
                            banner.style.display = 'none';
                            banner.remove();
                        }
                
                    // Method 3: Find parent containers and remove
                    const containers = document.querySelectorAll('[class*="consent"], [class*="cookie"]');
                        containers.forEach(container => {
                            if (container.innerHTML.toLowerCase().includes('cookie') || 
                                container.innerHTML.toLowerCase().includes('consent')) {
                                container.remove();
                            }
                        });
                
                    // Method 4: Modify local storage
                    localStorage.setItem('consent-banner', 'true');
                    localStorage.setItem('twitch.gdpr.consent', 'true');
                
                    return "Attempted all banner removal methods";
                } catch (e) {
                    return "Error: " + e.message;
                    }
                """)
        
            logging.info(f"Direct manipulation result: {result}")
        
            # Verify banner removal
            try:
                # Use multiple selectors to verify banner is gone
                selectors = [
                    ".consent-banner",
                    "[class*='consent-banner']",
                    "[class*='cookie-banner']",
                    "[class*='gdpr']"
                ]
            
                for selector in selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logging.warning(f"Found {len(elements)} elements matching {selector}")
                    
                        # Try one last time to force remove them
                        self.driver.execute_script("""
                            const elements = document.querySelectorAll(arguments[0]);
                                elements.forEach(el => {
                                    el.style.display = 'none';
                                    el.remove();
                                });
                        """, selector)
            
                # Verify one final time
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".consent-banner")))
                logging.info("Banner successfully removed")
                return True
            
            except TimeoutException:
                # Get final state of the page
                page_state = self.driver.execute_script("""
                    return {
                        cookies: document.cookie,
                        localStorage: Object.keys(localStorage)
                            .filter(key => key.includes('consent') || key.includes('cookie'))
                            .reduce((obj, key) => {
                                obj[key] = localStorage.getItem(key);
                                return obj;
                            }, {}),
                        visibleBanners: Array.from(document.querySelectorAll('[class*="consent"], [class*="cookie"]'))
                            .map(el => ({
                            className: el.className,
                            visible: window.getComputedStyle(el).display !== 'none'
                        }))
                    };
                """)
            
                logging.error(f"Failed to remove banner. Page state: {page_state}")
            
                # Try to bypass by injecting click into the React event system
                bypass_result = self.driver.execute_script("""
                    // Find React root
                    const root = document.querySelector('[class*="Layout-sc"]')?.__react_root;
                        if (!root) return "No React root found";
                
                        // Try to find and trigger the accept handler
                        const button = document.querySelector('button[data-a-target="consent-banner-accept"]');
                            if (!button) return "No button found";
                
                            // Simulate React synthetic event
                            const event = new Event('click', { bubbles: true, cancelable: true });
                            Object.defineProperty(event, '_reactName', { value: 'onClick' });
                            button.dispatchEvent(event);
                
                        return "Attempted React event bypass";
                    """)
            
                logging.info(f"React bypass result: {bypass_result}")
            
                # One final check
                #time.sleep(2)
                
                final_check = self.driver.execute_script("""
                    return document.querySelector('.consent-banner') === null;
                """)
                return final_check
            
        except Exception as e:
            logging.error(f"Error in cookie consent handling: {str(e)}")
            return False