import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import csv
import requests
import os

def write_price_to_csv(hotel_price,filename="prices/sterlingmac_hotel_prices.csv"):
    # checkin = today, checkout = tomorrow
    hotel_price = hotel_price if hotel_price != "" else "NA"
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    checkin_date = today.strftime("%Y-%m-%d")
    checkout_date = tomorrow.strftime("%Y-%m-%d")

    if hotel_price == 0:
        hotel_price = "No Vacancies"
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


def print_div_html(driver, xpath):
    from bs4 import BeautifulSoup

    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print("HTML contents of the div:")
        print(element.get_attribute("outerHTML"))
    except Exception as e:
        print(f"[ERROR] Could not find or print div HTML: {e}")
        # Save root DOM as RootDOM.html
        root_html = driver.page_source
        with open("RootDOM.html", "w", encoding="utf-8") as f:
            f.write(root_html)
        print("[INFO] Saved root DOM as RootDOM.html")

        # Parse RootDOM.html and extract all matching divs
        with open("RootDOM.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            price_divs = soup.find_all("div", class_="current-price fs12 fw600 notranslate")
            if price_divs:
                print("Extracted alternate data from RootDOM.html:")
                for idx, div in enumerate(price_divs):
                    if idx % 2 == 0:  # Print alternate ones (0, 2, 4, ...)
                        print(div.get_text(strip=True))
                        text=div.get_text(strip=True)
                        # Extract numeric value from text
                        number = text.replace("INR ", "").replace(",", "").strip()
                        write_price_to_csv(number)
            else:
                print("[INFO] No vacancies")
                write_price_to_csv(0)

                

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
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        checkin_date = today.strftime("%m-%d-%Y")
        checkout_date = tomorrow.strftime("%m-%d-%Y")

        base_url = "https://www.swiftbook.io"
        time.sleep(20)
        print(base_url + f"/inst/#home?propertyId=54804&checkIn={checkin_date}&checkOut={checkout_date}&noofrooms=1&adult0=1&child0=0&promoCode=")
        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + f"/inst/#home?propertyId=54804&checkIn={checkin_date}&checkOut={checkout_date}&noofrooms=1&adult0=1&child0=0&promoCode=")
        # set window size
        #driver.get(base_url + '/')
        driver.set_window_size(1400, 843)
        print("set window size")
        #wait_find(driver, """css=.doc-title""").click()
        #driver.find_element(*find_by("""css=.check-availability:nth-child(1)""")).click()
        

        #wait = WebDriverWait(driver, 20)
        #wait_find(driver, """css=.btn > .wmr-cl-icon""").click()
        #print("removed left bottom pop up")
        #wait_find(driver, """css=.lucide""").click()
        #print("removed right bottom pop up")
        
        time.sleep(7)
       

        #xpath = """//h3[contains(@class, 'roomtype')]"""
        xpath = """//*[@id="roomImgSliderWrapper"]/../div/div[2]/span[2]"""
        #xpath = """"//*[@id="app"]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/span[2]"""
        #xpath= """/html"""
        print_div_html(driver, xpath)
        sys.exit(1)       
        # --- END GENERATED CODE ---
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
