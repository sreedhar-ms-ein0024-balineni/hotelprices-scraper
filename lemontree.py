import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime, timedelta
import requests

def write_price_to_csv(hotel_price,filename="prices/lemontree_hotel_prices.csv"):
    hotel_price = hotel_price if hotel_price != "" else "NA"
    # checkin = today, checkout = tomorrow
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    checkin_date = today.strftime("%Y-%m-%d")
    checkout_date = tomorrow.strftime("%Y-%m-%d")
    
    # detect time
    time_detected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # detect ISP/public IP
    try:
        isp_ip = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        isp_ip = "unknown"
    
    # write to CSV
    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        # Write header only if file is empty
        if f.tell() == 0:
            writer.writerow(["checkin_date", "checkout_date", "hotel_price", "time_detected" , "ISP_IP"])
        
        writer.writerow([checkin_date, checkout_date, hotel_price, time_detected, isp_ip])




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
        print("=================================== LEMON TREE HOTELS ===============================================")
        base_url = "https://lemontreebengaluru.reserve.pegsbe.com"
        # --- BEGIN GENERATED CODE ---
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        checkin_date = today.strftime("%Y-%m-%d")
        checkout_date = tomorrow.strftime("%Y-%m-%d")

        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + f"/rooms?Rooms=1&hotel=BLRLTH&CheckinDate={checkin_date}&LOS=1&Adults_1=1&Children_1=0&locale=en&Currency=INR&offerCode=")
        # Error in command setWindowSize: list index out of range
        driver.execute_script('window.scrollTo(0,213)')


        # wait = WebDriverWait(driver, 60)
        #  element = wait.until(EC.text_to_be_present_in_element((By.XPATH, """//*[@id="bedType-EXEK"]/div/div/div[2]/div/div[1]/div[1]/div/del/span[2]"""),'' ))
        #  hotel_price = wait_find(driver, """xpath=//*[@id="bedType-EXEK"]/div/div/div[2]/div/div[1]/div[1]/div/del/span[2]""").text
        #  span_elements = driver.find_elements(By.XPATH, """//*[@id="bedType-EXEK"]/div/div/div[2]/div/div[1]/div[1]/div/del/span[2]""")
        # for span in span_elements:
        #     text = span.text
        #     print(text) 
        # print(hotel_price)
        # print("hotel price printed")


        time.sleep(5.0)
        #currentPrice = driver.find_element(*find_by("""xpath=//strong[./span[text()="Current Price"]]//span[3]""")).text
        xpath = '//strong[./span[text()="Current Price"]]//span[3]'
        elements = driver.find_elements(By.XPATH, xpath)    
        for el in elements:
            price_text = el.text.strip() 
            clean_price = price_text.replace(",", "").replace('"', "")
            write_price_to_csv(clean_price)
            print(el.text)

        #print("Done")
        # --- END GENERATED CODE ---
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

