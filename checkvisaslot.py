# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 20:10:47 2022

@author: Vishaal Sudarsan
"""

import time
import os
import sys
import urllib
import pytesseract
import requests
from contextlib import contextmanager
from datetime import datetime
from pytz import timezone
from PIL import Image
from pytesseract import image_to_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    with suppress_stdout():
        browser = webdriver.Chrome(options = chrome_options, service=Service(ChromeDriverManager().install()))
        browser.delete_all_cookies()
        browser.get("https://checkvisaslots.com/pro.html")
    print("1.Loaded Website\n")
    time.sleep(60)
    element = browser.find_element(By.XPATH, "//*[@id='api_key']")
    element.send_keys("H4BXV7")
    element = browser.find_element(By.XPATH, "//*[contains(text(), 'Submit')]")
    element.click()
    print("2.Submitted Access Key\n")
    time.sleep(100)
    #browser.get_screenshot_as_file("screenshot.png")
    #element = browser.find_element(By.XPATH, "//*[contains(text(), 'Retrieve')]")
    time.sleep(60)
    element = browser.find_element(By.XPATH, "//*[@id='view_txn']")
    element.send_keys("\n")
    print("3.Clicked Retrieve Button\n")
    time.sleep(60)
    #browser.get_screenshot_as_file("screenshot.png")
    current_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    
    
    for i in range(1, 13):
        xpath = '/html/body/section[2]/div/div[4]/div[' + str(i) + ']/a/img'
        img = browser.find_element_by_xpath(xpath)
        src = img.get_attribute('src')
        image_name = "image" + str(i)+".png"
        urllib.request.urlretrieve(src, image_name)
        image = Image.open(r'C:\Users\Vishaal Sudarsan\Documents\Python Files\Visa Slot Availability\image' + str(i) + '.png', mode='r')
        text = image_to_string(image)
        if "Select interview location : CHENNAI VAC" in text:
            if "Available" in text:
                slot_text = str.split(text, "Available")[1]
                slot_text = str.split(slot_text, "checkvisaslots.com")[0]
                print("\n\n", slot_text, "\n\n")
                break
            else:
                slot_text = "slot not available as of " + str(current_time)
    
    bot_token = '5307676822:AAH1YtysF_fcrawTYqARgJutMO6i8SAIttI'
    bot_chatIDs = ['1792910115' ]
    if "2022" in slot_text:
        bot_chatIDs.append( '1845791184' )
    for bot_chatID in bot_chatIDs:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + slot_text
        response = requests.get(send_text)
        print(response.json())
    time.sleep(300)
    
while True:
    try:
        main()
    except Exception as e:
        print(e)
        continue