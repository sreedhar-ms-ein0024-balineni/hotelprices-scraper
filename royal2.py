import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def find_by(target):
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

def wait_find(driver, selector, timeout=30):
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, timeout).until(lambda d: d.find_element(*find_by(selector)))
def main():
    options = Options()
    options.headless = True 
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.add_argument("--start-maximized")
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )
    driver = webdriver.Firefox(options=options)
    try:

        base_url = "https://www.royalorchidhotels.com"
        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + '/')
        # Error in command setWindowSize: list index out of range
        webdriver.ActionChains(driver).move_to_element(wait_find(driver, """css=.ls-is-cached""")).perform()
        wait_find(driver, """css=.memberCloseBtn""").click()
        wait_find(driver, """id=BookingEngine_DdlCity""").click()
        from selenium.webdriver.support.ui import Select
        Select(wait_find(driver, """id=BookingEngine_DdlCity""")).select_by_visible_text('Bangalore')
        webdriver.ActionChains(driver).move_to_element(wait_find(driver, """css=a > .ls-is-cached""")).perform()
        # Unsupported command: mouseOut
        wait_find(driver, """id=BookingEngine_DdlHotel""").click()
        from selenium.webdriver.support.ui import Select
        Select(wait_find(driver, """id=BookingEngine_DdlHotel""")).select_by_visible_text('Hotel Royal Orchid, Bangalore')
        driver.find_element(*find_by("""css=#BookingEngine_DdlHotel > option:nth-child(2)""")).click()
        wait_find(driver, """id=adut""").click()
        print("almost")
        from selenium.webdriver.support.ui import Select
        Select(wait_find(driver, """id=adut""")).select_by_visible_text('1')
        driver.find_element(*find_by("""css=#adut > option:nth-child(2)""")).click()
        wait_find(driver, """id=bth""").click()
        # Unsupported command: selectWindow
        driver.switch_to.window(driver.window_handles[-1])

        #wait_find(driver, "xpath=//button[@title='Check Availability']").click()
        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Check Availability']")))
        button.click()
        print("check availability clicked")

        # wait_find(driver, """css=#js-rate-98978-29459-106577 > #rate-plan-responsive .discount-price > span""").click()
        # driver.find_element(*find_by("""css=.fa-times:nth-child(2)""")).click()
        # wait_find(driver, """css=.fa-chevron-right""").click()
        # wait_find(driver, """css=#js-rate-98978-29459-106577 > #rate-plan-responsive .discount-price > span""").click()
        # wait_find(driver, """css=#js-rate-98978-29459-106577 > #rate-plan-responsive .discount-price > span""").click()
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="room-thumbnail-rate-detail"]/div/div[2]/div[2]/span'),'' ))
        hotel_price = wait_find(driver, """xpath=//*[@id="room-thumbnail-rate-detail"]/div/div[2]/div[2]/span""").text
        span_elements = driver.find_elements(By.XPATH, '//*[@id="room-thumbnail-rate-detail"]/div/div[2]/div[2]/span')
        for span in span_elements:
            text = span.text.strip()
            print(text) 
        print(hotel_price)
        print("hotel price printed")
        # --- END GENERATED CODE ---
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

