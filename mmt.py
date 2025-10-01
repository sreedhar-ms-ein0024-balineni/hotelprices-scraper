import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def find_by(target):
    print("Finding by:", target)
    if target.startswith('css='):
        return (By.CSS_SELECTOR, target[4:])
    elif target.startswith('id='):
        return (By.ID, target[3:])
    elif target.startswith('xpath='):
        return (By.XPATH, target[6:])
    elif target.startswith('name='):
        return (By.NAME, target[5:])
    elif target.startswith('linkText='):
        return (By.LINK_TEXT, target[9:])
    elif target.startswith('partialLinkText='):
        return (By.PARTIAL_LINK_TEXT, target[17:])
    else:
        return (By.CSS_SELECTOR, target)

def wait_find(driver, selector, timeout=10):
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, timeout).until(lambda d: d.find_element(*find_by(selector)))
def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    try:

        base_url = "https://www.makemytrip.com"
        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + '/')
        # Error in command setWindowSize: list index out of range
        time.sleep(2.0)
        wait_find(driver, """css=.commonModal__close""").click()
        wait_find(driver, """css=.chHotels""").click()
        wait_find(driver, """id=city""").click()
        el = wait_find(driver, """css=.react-autosuggest__input""")
        el.clear()
        el.send_keys('Taj Krishna, Hyderabad')
        wait_find(driver, """css=#react-autowhatever-1-section-0-item-1 > .clickable""").click()
        wait_find(driver, """xpath=//div[@aria-label='Mon Sep 29 2025']""").click()
        wait_find(driver, """xpath=//div[@aria-label='Tue Sep 30 2025']""").click()
        wait_find(driver, """css=.btnApplyNew""").click()
        driver.save_screenshot("after_date_selection.png")
        wait_find(driver, """id=hsw_search_button""").click()
        driver.save_screenshot("after_search_click.png")
        time.sleep(5)
        rate = wait_find(driver, """id=hlistpg_hotel_shown_price""").text
        print(rate)
        driver.close()
        # --- END GENERATED CODE ---
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
