import logging
import os
import time
import shutil
from behave import *
from main.utils.platform_handling import PlatformHandling
from main.utils.test_report import TestReport
import allure

# Create an instance of the TestReport class
test_report = TestReport()
logging.info("TestReport instance created")

def before_scenario(context, scenario):
    """Hook that runs before each scenario"""
     # Get the tag from the environment variable
    tag = os.environ.get("platform", '')  # Fetch the value of TEST_TAG from environment variable
    environment = os.environ.get("environment", '')  # Fetch the value of TEST_TAG from environment variable
    if not tag:
        logging.error("No tag provided, cannot determine the platform.")
        raise ValueError("No tag provided in the environment variable")

    # Delete appropriate allure-results folder based on platform tag
    allure_dir = f'allure-results-{tag}'
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
        logging.info(f"Deleted existing {allure_dir} folder")

    # Default platform to an empty string
    platform = ''

    logging.info(f"Tags found in scenario: {tag}")
    if (tag=='@android'):
        platform = 'android'
    elif (tag=='@ios'):
        platform = 'ios'
    elif (tag=='@website'):
        platform = 'website'

    context.platform = platform  # Set the platform to context

    if platform:
        # Initialize platform handler and get driver
        logging.info(f"Initializing platform handler for {platform}")
        platform_handler = PlatformHandling(platform, environment, scenario)
        context.driver = platform_handler.get_driver()
        logging.info("Driver initialized successfully")
    else:
        logging.error("No valid platform tag found")
        raise ValueError("No valid platform tag (@android, @ios, or @website) found")


def after_scenario(context, scenario):
    """Hook that runs after each scenario"""
    logging.info(f"Running after_scenario hook for scenario: {scenario.name}")
    
    # Update LambdaTest status
    if hasattr(context, 'lambda_method'):
        status = "passed" if scenario.status == "passed" else "failed"
        if scenario.status == "skipped":
            status = "skipped"
        context.lambda_method.update_test_status(status)

    # Existing code for reporter and screenshots
    if hasattr(context, 'reporter'):
        if scenario.status == "passed":
            context.reporter.add_pass()
            logging.info("Scenario passed")
        elif scenario.status == "failed":
            context.reporter.add_fail()
            logging.error("Scenario failed")
        elif scenario.status == "skipped":
            context.reporter.add_skip()
            logging.warning("Scenario skipped")
    
    # Take screenshot for failed scenarios
    if hasattr(context, 'driver') and scenario.status == "failed":
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name="Scenario Failed",
            attachment_type=allure.attachment_type.PNG
        )

def after_all(context):
    """Hook that runs after all scenarios have completed"""
    if hasattr(context, 'driver'):
        context.driver.quit()
        logging.info("Driver quit after all scenarios.")
    
    # After all tests are complete, print the final report
    logging.info("Generating final test report")
    test_report.print_report()


# adding reporting to take screenshot if the step fails
def after_step(context, step):
    if step.status == "failed":
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"screenshot_{step.name}_{timestamp}.png"
        context.driver.save_screenshot(screenshot_name)
        logging.error(f"Step failed. Screenshot saved as {screenshot_name}")
