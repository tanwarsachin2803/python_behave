import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from main.utils.locator_retrievel.locator_retrieved import LocatorRetrieved
from main.utils.platform_handling import PlatformHandling
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given(u'the user opens the website')
def step_impl(context):
    context.driver.get("https://f10boxing.weebly.com/reserve.html#/create-account")
    context.driver.maximize_window()

@given(u'the user switches to iframe {frame_locator} on {page_name}')
def step_impl(context, frame_locator, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    frame_element = lr.get_element(frame_locator)
    context.driver.switch_to.frame(frame_element)

@then(u'the user clicks {existence} on {locator} on {page_name}')
def step_impl(context, existence, locator, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    existence = existence.lower().replace('"', '')
    try:
        element = lr.get_element(locator)
        element.click()
    except Exception as e:
        if existence == "surely":
            raise Exception(f"Element {locator} was not found but was expected to exist")
        elif existence == "maybe":
            # Element doesn't exist but that's okay since it was optional
            pass
        else:
            raise ValueError(f"Invalid existence value '{existence}'. Must be one of: surely, maybe")

@then(u'the user should see {expected_text} on {locator} on {page_name}')
def step_impl(context, expected_text, locator, page_name):
    pass

@then(u'the user enters {text} in {locator} on {page_name}')
def step_impl(context, text, locator, page_name):
    # Pass context.platform to LocatorRetrieved class
    text=(text.lower()).replace('"', '')
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    element = lr.get_element(locator)
    element.send_keys(text)

@then(u'the user clicks on enter')
def step_impl(context):
    context.driver.send_keys(Keys.ENTER)

@then(u'the user verifies {locator} is {state} on {page_name}')
def step_impl(context, locator, state, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    element = lr.get_element(locator)
    state=(state.lower()).replace('"', '')
    if state == "visible":
        assert element.is_displayed(), f"Element {locator} is not visible"
    elif state == "not-visible":
        assert not element.is_displayed(), f"Element {locator} is visible but should not be"
    elif state == "enabled":
        assert element.is_enabled(), f"Element {locator} is not enabled"
    elif state == "disabled":
        assert not element.is_enabled(), f"Element {locator} is enabled but should be disabled"
    else:
        raise ValueError(f"Invalid state '{state}'. Must be one of: visible, not-visible, enabled, disabled")

@then(u'the user gets text from {locator} on {page_name}')
def step_impl(context, locator, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    element = lr.get_element(locator)
    context.element_text = element.text

@then(u'the user {state} compare {expected_text} of {locator} on {page_name}')
def step_impl(context, state, expected_text, locator, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    element = lr.get_element(locator)
    actual_text = element.text
    if state == "exactly":
        assert actual_text == expected_text, f"Expected text '{expected_text}' but got '{actual_text}'"
    elif state == "contains":
        assert expected_text in actual_text, f"Text '{expected_text}' not found in '{actual_text}'"
    else:
        raise ValueError(f"Invalid state '{state}'. Must be one of: exactly, contains")

@then(u'the user scrolls to {locator} on {page_name}')
def step_impl(context, locator, page_name):
    lr = LocatorRetrieved(context.driver, page_name, context.platform)
    element = lr.get_element(locator)
    context.driver.execute_script("arguments[0].scrollIntoView(true);", element)


@then(u'the user enters {numbers} on the keyboard')
def step_impl(context, numbers):
    # Convert string numbers to list of individual digits
    digits = list(str((numbers.lower()).replace('"', '')))
    # For each digit, simulate keyboard press
    for digit in digits:
        if context.platform == "android":
            context.driver.press_keycode(int(digit) + 7)  # Android keycode for 0-9 are 7-16
        elif context.platform == "ios":
            context.driver.execute_script('mobile: pressButton', {'name': digit}) 
        else:
            context.driver.find_element_by_tag_name('body').send_keys(digit)  # Assuming keyboard input on the body or focused input field

@then(u'the user clicks {locator} at coordinates {x:d} and {y:d}')
def step_impl(context, x, y):
    """
    Click at specific x,y coordinates on the screen
    
    :param context: The behave context
    :param x: X coordinate to click (integer)
    :param y: Y coordinate to click (integer)
    """
    if context.platform in ["android", "ios"]:
        actions = ActionChains(context.driver)
        actions.move_by_offset(x, y).click().perform()
    else:
        # For web, use JavaScript to create and trigger a click event
        context.driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")

@then(u'the user waits for {seconds} seconds')
def step_impl(context, seconds):
    """
    Pause execution for specified number of seconds using time.sleep()
    :param context: The behave context
    :param seconds: Number of seconds to sleep (will be converted from string)
    """
    # Remove quotes and convert to float to handle decimal seconds
    seconds = float(str(seconds).replace('"', ''))
    time.sleep(seconds)




# @then(u'the user clicks on "google_search_button" on "landing_page"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then the user clicks on "google_search_button" on "landing_page"')