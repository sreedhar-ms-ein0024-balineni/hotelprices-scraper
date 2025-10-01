# Selenium IDE command to Python mapping for robust conversion
def open_command(t, v):
    # If t starts with '/', append to base_url
    return "driver.get(base_url + '{0}')".format(t) if t.startswith('/') else f"driver.get('{t}')"

COMMAND_MAP = {
    'open': open_command,
    'click': lambda t, v: f"driver.find_element(*find_by('{t}')).click()",
    'clickAt': lambda t, v: f"driver.find_element(*find_by('{t}')).click()  # clickAt ignores coordinates",
    'doubleClick': lambda t, v: f"webdriver.ActionChains(driver).double_click(driver.find_element(*find_by('{t}'))).perform()",
    'type': lambda t, v: f"el = driver.find_element(*find_by('{t}'))\nel.clear()\nel.send_keys('{v}')",
    'sendKeys': lambda t, v: f"driver.find_element(*find_by('{t}')).send_keys('{v}')",
    'select': lambda t, v: f"from selenium.webdriver.support.ui import Select\nSelect(driver.find_element(*find_by('{t}'))).select_by_visible_text('{v}')",
    'check': lambda t, v: f"el = driver.find_element(*find_by('{t}'))\nif not el.is_selected(): el.click()",
    'uncheck': lambda t, v: f"el = driver.find_element(*find_by('{t}'))\nif el.is_selected(): el.click()",
    'assertText': lambda t, v: f"assert driver.find_element(*find_by('{t}')).text == '{v}'",
    'verifyText': lambda t, v: f"assert driver.find_element(*find_by('{t}')).text == '{v}'  # verifyText",
    'assertTitle': lambda t, v: f"assert driver.title == '{v}'",
    'verifyTitle': lambda t, v: f"assert driver.title == '{v}'  # verifyTitle",
    'assertElementPresent': lambda t, v: f"assert driver.find_element(*find_by('{t}')) is not None",
    'assertElementNotPresent': lambda t, v: f"try:\n    driver.find_element(*find_by('{t}'))\n    assert False, 'Element should not be present'\nexcept Exception: pass",
    'waitForElementPresent': lambda t, v: f"from selenium.webdriver.support.ui import WebDriverWait\nWebDriverWait(driver, 10).until(lambda d: d.find_element(*find_by('{t}')))",
    'waitForElementVisible': lambda t, v: f"from selenium.webdriver.support.ui import WebDriverWait\nWebDriverWait(driver, 10).until(lambda d: d.find_element(*find_by('{t}')).is_displayed())",
    'pause': lambda t, v: f"time.sleep({float(v) / 1000})",
    'store': lambda t, v: f"{v} = driver.find_element(*find_by('{t}')).text",
    'storeValue': lambda t, v: f"{v} = driver.find_element(*find_by('{t}')).get_attribute('value')",
    'storeText': lambda t, v: f"{v} = driver.find_element(*find_by('{t}')).text",
    'mouseOver': lambda t, v: f"webdriver.ActionChains(driver).move_to_element(driver.find_element(*find_by('{t}'))).perform()",
    'dragAndDropToObject': lambda t, v: f"webdriver.ActionChains(driver).drag_and_drop(driver.find_element(*find_by('{t}')), driver.find_element(*find_by('{v}'))).perform()",
    'executeScript': lambda t, v: f"driver.execute_script('{t}')",
    'runScript': lambda t, v: f"driver.execute_script('{t}')",
    'setWindowSize': lambda t, v: f"driver.set_window_size({t.split(',')[0]}, {t.split(',')[1]})",
    'close': lambda t, v: f"driver.close()",
    'refresh': lambda t, v: f"driver.refresh()",
    'goBack': lambda t, v: f"driver.back()",
    'goForward': lambda t, v: f"driver.forward()",
    'echo': lambda t, v: f"print('{t}')",
    # Add more as needed
}

def find_by(target):
    # Heuristic: try to detect locator type
    if target.startswith('css='):
        return ('By.CSS_SELECTOR', target[4:])
    elif target.startswith('id='):
        return ('By.ID', target[3:])
    elif target.startswith('xpath='):
        return ('By.XPATH', target[6:])
    elif target.startswith('name='):
        return ('By.NAME', target[5:])
    elif target.startswith('linkText='):
        return ('By.LINK_TEXT', target[9:])
    elif target.startswith('partialLinkText='):
        return ('By.PARTIAL_LINK_TEXT', target[17:])
    else:
        # Default to CSS_SELECTOR
        return ('By.CSS_SELECTOR', target)
