import logging
from features.steps.common_steps import *  # Import common steps
import time
from behave import given, when, then
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import logging
import time

@then(u'the user enters {otp} using coordinates')
def step_impl(context, otp):
    """
    Enter OTP by clicking predefined coordinates
    
    :param context: The behave context
    :param otp: 6-digit OTP string
    """
    # Validate OTP is 6 digits
    otp = str(otp.replace('"', ''))
    if not otp.isdigit() or len(otp) != 6:
        raise ValueError("OTP must be exactly 6 digits")

    logging.info(f"OTP: {otp}")

    # Predefined coordinates for each click
    coordinates = [
        (414, 1823),
        (147, 1823), 
        (673, 1990),
        (155, 1640),
        (414, 1644),
        (414, 1644)
    ]

    # Click each coordinate
    for coord in coordinates:
        x, y = coord
        if context.platform in ["android", "ios"]:
            actions = TouchAction(context.driver)
            actions.tap(x=x, y=y).perform()  # Using touch action to tap at the specified coordinates
        else:
            context.driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")
        
        time.sleep(0.5)  # Small delay between clicks
