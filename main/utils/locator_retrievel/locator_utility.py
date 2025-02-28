from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LocatorUtil:
    @staticmethod
    def get_element(driver, locator_type, locator_value, timeout=10):
        """
        Returns the WebElement based on the provided locator type and value.
        Supports different types of locators such as id, xpath, etc.
        Waits for element visibility for specified timeout.
        
        :param locator_type: Type of locator (e.g., 'id', 'xpath', 'name', etc.)
        :param locator_value: The value of the locator (e.g., 'APjFqb', 'xpath=//input[@value="Google Search"]')
        :param timeout: Maximum time to wait for element visibility in seconds (default 10)
        :return: WebElement
        """
        if locator_type.lower() == 'id':
            return LocatorUtil.get_element_by_id(driver, locator_value, timeout)
        elif locator_type.lower() == 'xpath':
            return LocatorUtil.get_element_by_xpath(driver, locator_value, timeout)
        elif locator_type.lower() == 'name':
            return LocatorUtil.get_element_by_name(driver, locator_value, timeout)
        elif locator_type.lower() == 'class':
            return LocatorUtil.get_element_by_class_name(driver, locator_value, timeout)
        elif locator_type.lower() == 'css':
            return LocatorUtil.get_element_by_css_selector(driver, locator_value, timeout)
        else:
            raise ValueError(f"Locator type '{locator_type}' is not supported.")

    @staticmethod
    def get_element_by_id(driver, locator_value, timeout=10):
        """
        Retrieves element by ID with wait.
        
        :param locator_value: The ID value (e.g., 'APjFqb')
        :param timeout: Maximum time to wait for element visibility in seconds
        :return: WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.ID, locator_value)))

    @staticmethod
    def get_element_by_xpath(driver, locator_value, timeout=10):
        """
        Retrieves element by XPath with wait.
        
        :param locator_value: The XPath value (e.g., '//input[@value="Google Search"]')
        :param timeout: Maximum time to wait for element visibility in seconds
        :return: WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.XPATH, locator_value)))

    @staticmethod
    def get_element_by_name(driver, locator_value, timeout=10):
        """
        Retrieves element by Name with wait.
        
        :param locator_value: The Name value (e.g., 'search')
        :param timeout: Maximum time to wait for element visibility in seconds
        :return: WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.NAME, locator_value)))

    @staticmethod
    def get_element_by_class_name(driver, locator_value, timeout=10):
        """
        Retrieves element by Class Name with wait.
        
        :param locator_value: The class name value (e.g., 'btn-primary')
        :param timeout: Maximum time to wait for element visibility in seconds
        :return: WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, locator_value)))

    @staticmethod
    def get_element_by_css_selector(driver, locator_value, timeout=10):
        """
        Retrieves element by CSS Selector with wait.
        
        :param locator_value: The CSS selector value (e.g., '.btn-primary')
        :param timeout: Maximum time to wait for element visibility in seconds
        :return: WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator_value)))
