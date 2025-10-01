import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import csv
from datetime import datetime, timedelta
import requests


def find_by(target):
    print(target)
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
    print(f"Waiting for {selector}")
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, timeout).until(lambda d: d.find_element(*find_by(selector)))

def write_price_to_csv(hotel_price, rate_type,filename="prices/ginger_hotel_prices.csv"):
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
            writer.writerow(["checkin_date", "checkout_date", "hotel_price", "time_detected","rate_type" , "ISP_IP"])
        
        writer.writerow([checkin_date, checkout_date, hotel_price, time_detected, rate_type, isp_ip])

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

        base_url = "https://www.gingerhotels.com"
        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + '/hotels/ginger-bangalore-irr/rooms-and-suites/booking')
       
        # Error in command setWindowSize: list index out of range
        #driver.find_element(*find_by("""xpath=(//div[contains(@class,'MuiCollapse-wrapperInner') and contains(@class,'MuiCollapse-horizontal')]//div[contains(@class,'MuiStack-root')])[1]""")).click()
        #ait_find(driver, """xpath=//abbr[@aria-label='29 September 2025']""").click()
        time.sleep(7)
        #wait_find(driver, """xpath=//abbr[@aria-label='30 September 2025']""").click()
        #wait_find(driver, """css=.MuiButton-gradient-contained""").click()
        #emberRate = wait_find(driver, """xpath=//div[@aria-label='tabs']//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]//span[2]""").text
        #print(memberRate)

        xpath = '//div[@aria-label="MemberRateDetails"]/div/span[2]'
        elements = driver.find_elements(By.XPATH, xpath)    
        for el in elements:
            text = el.text.strip()
            number = text.replace("₹", "").replace(",", "")
            write_price_to_csv(number,"Membership") 
            #print(number)

        xpath = '//div[@aria-label="StandardRateDetails"]/div/span[2]'
        elements = driver.find_elements(By.XPATH, xpath)    
        for el in elements:
            text = el.text.strip()
            number = text.replace("₹", "").replace(",", "")
            write_price_to_csv(number,"Standard") 
            #print(number)

        #print("Done")
        driver.close()
        # --- END GENERATED CODE ---
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

