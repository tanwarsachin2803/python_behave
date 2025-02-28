import json
import logging
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from appium import webdriver as appium_webdriver  # Appium for Android/iOS
from main.utils.json_reader import JSONReader
from main.utils.lambda_basic_methods import LambdaBasicMethod  # Assuming the JSONReader class is in the utils folder

class PlatformHandling:
    def __init__(self, platform, environment, scenario):
        self.platform = platform
        self.environment = environment
        self.scenario = scenario
        logging.info(f"Initializing PlatformHandling for platform: {platform} and environment: {environment}")
        self.capabilities = self.load_capabilities(platform, environment)
        self.lambda_method = LambdaBasicMethod(platform=platform, environment=environment)
        logging.info("PlatformHandling initialization complete")

    def load_capabilities(self, platform, environment):
        """
        Loads the capabilities using the JSONReader class based on the platform and environment (local or lambda).
        """
        logging.info(f"Loading capabilities for platform: {platform}, environment: {environment}")
        platform = platform.lower().replace('"', '')
        environment = environment.lower().replace('"', '')
        capabilities_path = f"main/utils/device_capabilities/{platform}.json"
        logging.debug(f"Reading capabilities from: {capabilities_path}")
        json_reader = JSONReader(capabilities_path)
        capabilities = json_reader.get_value(environment)
        if not capabilities:
            logging.error(f"No capabilities found for platform '{platform}' and environment '{environment}'")
            raise ValueError(f"No capabilities found for platform '{platform}' and environment '{environment}'")

        logging.debug(f"Loaded capabilities: {capabilities}")
        logging.info("Capabilities loaded successfully")
        return capabilities

    def get_driver(self):
        """
        Returns a WebDriver instance based on platform capabilities (Android/iOS/Website).
        """
        logging.info(f"Getting driver for platform: {self.platform}")
        if self.platform == "android" and self.environment == "virtual":
            logging.info("Initializing virtual Android driver on LambdaTest")
            capabilities = self.capabilities
            if self.environment == "virtual":
                capabilities["name"] = self.scenario.name
            logging.info(f"Capabilities: {capabilities}")
            json_reader_lambda = JSONReader("main/utils/device_capabilities/lambda_capabilities.json")
            lambda_username = json_reader_lambda.get_value("username")
            lambda_access_key = json_reader_lambda.get_value("accessKey")
            logging.debug("Lambda credentials loaded successfully")
            driver = webdriver.Remote(
                command_executor=f"https://{lambda_username}:{lambda_access_key}@mobile-hub.lambdatest.com/wd/hub",
                desired_capabilities=capabilities
            )
            logging.info(f"Driver initialized successfully for Android on LambdaTest")
            self.lambda_method.set_driver(driver)
            return driver
        elif self.platform == "android":
            return self.start_android_driver()
        elif self.platform == "ios":
            return self.start_ios_driver()
        elif self.platform == "website":
            return self.start_website_driver()
        else:
            logging.error(f"Unsupported platform: {self.platform}")
            raise ValueError(f"Unsupported platform: {self.platform}")

    def start_android_driver(self):
        # Initialize the Appium driver for Android
        logging.info("Starting Android driver")
        capabilities = self.capabilities
        logging.info(f"Capabilities: {capabilities}")
        logging.info(f"Environment: {self.environment}")
        try:
            if self.environment == "local":
                logging.info("Starting local Android driver")
                driver = appium_webdriver.Remote(
                    command_executor=f"http://127.0.0.1:4723/wd/hub",
                    desired_capabilities=capabilities
                )
                logging.info("Local Android driver started successfully")
                return driver
            else:
                logging.info("Starting remote Android driver on LambdaTest")
                json_reader_lambda = JSONReader("main/utils/device_capabilities/lambda_capabilities.json")
                lambda_username = json_reader_lambda.get_value("username")
                lambda_access_key = json_reader_lambda.get_value("accessKey")
                logging.debug("Lambda credentials loaded successfully")
                driver = appium_webdriver.Remote(
                    command_executor=f"https://{lambda_username}:{lambda_access_key}@mobile-hub-apac.lambdatest.com/wd/hub",
                    desired_capabilities=capabilities
                )
                logging.info("Remote Android driver started successfully")
                return driver
        except Exception as e:
            logging.error(f"Failed to start Android driver: {e}")
            raise

    def start_ios_driver(self):
        # Initialize the Appium driver for iOS
        logging.info("Starting iOS driver")
        capabilities = self.capabilities
        try:
            logging.info("Connecting to Appium server for iOS")
            driver = appium_webdriver.Remote(
                command_executor=f"http://127.0.0.1:4723/wd/hub",
                desired_capabilities=capabilities
            )
            logging.info("iOS driver started successfully")
            return driver
        except Exception as e:
            logging.error(f"Failed to start iOS driver: {e}")
            raise

    def start_website_driver(self):
        # Initialize the Selenium WebDriver for Website
        logging.info("Starting website driver")
        capabilities = self.capabilities
        try:
            if capabilities['browserName'] == 'chrome':
                # Use WebDriverManager to get the correct version of ChromeDriver
                logging.info("Initializing Chrome driver")
                driver = webdriver.Chrome(ChromeDriverManager().install())
                logging.info("Chrome driver initialized successfully")
            elif capabilities['browserName'] == 'firefox':
                # Use WebDriverManager to get the correct version of GeckoDriver
                logging.info("Initializing Firefox driver")
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
                logging.info("Firefox driver initialized successfully")
            elif capabilities['browserName'] == 'safari':
                # Safari WebDriver is built into macOS, so we can directly use it
                logging.info("Initializing Safari driver")
                driver = webdriver.Safari()    
                logging.info("Safari driver initialized successfully")
            else:
                logging.error(f"Unsupported browser: {capabilities['browserName']}")
                raise ValueError(f"Unsupported browser: {capabilities['browserName']}")
            
            logging.info(f"Website driver started successfully for {capabilities['browserName']}")
            return driver
        except Exception as e:
            logging.error(f"Failed to start website driver: {e}")
            raise
