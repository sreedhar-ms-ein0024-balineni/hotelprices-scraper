#!/usr/bin/env python3

import time
import sys
import csv
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ( NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException)


def extract_number(rewardsRate: str) -> int:
    """
    Cleans the rewardsRate string and extracts the main number.
    Example: "4,500\n00" -> 4500
    """
    # Remove commas, newlines, spaces
    cleaned = rewardsRate.replace(",", "").replace("\n", "").replace(" ", "")

    # Drop the last 2 digits (the "00" part)
    number = cleaned[:-2]

    return int(number)

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


def write_price_to_csv(hotel_price, rate_type,filename="/opt/hotelprices-scraper/prices/ramada_encore_hotel_prices.csv"):
    # checkin = today, checkout = tomorrow
    hotel_price = hotel_price if hotel_price != "" else "NA"
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
        if f.tell() == 0 and rate_type != "no_vacancies":
            writer.writerow(["checkin_date", "checkout_date", "hotel_price", "time_detected","rate_type" , "ISP_IP"])
        
        if rate_type != "no_vacancies":
            writer.writerow([checkin_date, checkout_date, hotel_price, time_detected, rate_type, isp_ip])

        if rate_type == "no_vacancies":
            writer.writerow([checkin_date, checkout_date, rate_type, time_detected, rate_type, isp_ip])



def wait_find(driver, selector, timeout=10):
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, timeout).until(lambda d: d.find_element(*find_by(selector)))
def main():
    options = Options()
    options.headless = True  
    options.binary_location = "/usr/bin/firefox"
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.add_argument("--start-maximized")
    driver = webdriver.Firefox(options=options)
    try:
        print("================================== RAMADA ENCORE HOTELS ==============================================")
        base_url = "https://www.wyndhamhotels.com"
        # --- BEGIN GENERATED CODE ---
        driver.get(base_url + '/ramada/h-b-c-s-layout-bangalore-india/ramada-encore-bangalore-domlur/overview')
        # Error in command setWindowSize: list index out of range
        time.sleep(2.0)
        wait_find(driver, """xpath=//nav[@id='bookingBar__mini']/div/div/div/div/button/div""").click()
        #wait_find(driver, """xpath=//td[@id='date1759084200000']/a""").click()
        #wait_find(driver, """xpath=//td[@id='date1759170600000']""").click()
        time.sleep(2.0)
        try:
            wait_find(driver, """xpath=//nav[@id='bookingBar__mini']/div/div/div[5]/button""").click() # Search Button
        except ElementNotInteractableException:
            print("No vacancies available")
            write_price_to_csv(0 , "no_vacancies")
            sys.exit(0)
        #wait_find(driver, """xpath=//nav[@id='bookingBar__mini']/div/div/div[5]/button""").click()
        standardRate = wait_find(driver, """xpath=//ul[@id='general-rate-list']/li[3]/div[2]/div/div/div""").text
        rewardsRate = wait_find(driver, """xpath=//ul[@id='general-rate-list']/li[4]/div[2]/div/div/div""").text
        dinnerRate = wait_find(driver, """xpath=//ul[@id='general-rate-list']/li[6]/div[2]/div/div/div""").text
        #print(extract_number(standardRate))
        #print(extract_number(rewardsRate))
        #print(extract_number(dinnerRate))
        write_price_to_csv(extract_number(standardRate), "standard")
        write_price_to_csv(extract_number(dinnerRate), "dinner")
        write_price_to_csv(extract_number(rewardsRate), "reward")
        driver.close()
        # --- END GENERATED CODE ---
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
