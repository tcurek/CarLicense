from ast import Break
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import schedule


def play_alarm():
    msg = "Steffi I Found an appointment"
    for i in range(3):
        os.system(f'spd-say "{msg}"')
        time.sleep(2)


def navigate_to_calendar(browser):
    button = browser.find_element(By.XPATH, '//html/body/div[4]/div[1]/div[2]/form/fieldset/input[2]')
    button.click()


def init_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.get('https://terminvereinbarung.muenchen.de/fs/termin/?loc=FS&ct=1071898')
    return browser


def available_appointments(browser):
    dayOptions = [day for day in browser.find_elements(By.CLASS_NAME,'nat_calendar') if day.tag_name == 'td'] 
    appointmentsFound = 0

    for day in dayOptions:
        contents = day.find_elements(By.TAG_NAME, 'a')

        if len(contents) > 0:
            appointmentsFound+=1
            print(f'Day: {day.text}')
            
    return appointmentsFound


def job(duration):
    print('Job running...')
    start = time.time()
    end = start

    while(end - start < duration):
        browser = init_browser()
        time.sleep(3)

        navigate_to_calendar(browser)
        countOfAppointments = available_appointments(browser)

        time.sleep(1)
        browser.close()

        if countOfAppointments < 1:
            print(f'{datetime.now()} : No Appointment found')
        else:
            print(f'{datetime.now()} : {countOfAppointments} appointments found')
            play_alarm()
            break

        time.sleep(60*3)
        end = time.time()
    
    print('Job ending...')


def Job2():
    print('Job running...')
    browser = init_browser()
    time.sleep(3)

    navigate_to_calendar(browser)
    countOfAppointments = available_appointments(browser)

    time.sleep(2)
    browser.close()

    if countOfAppointments < 1:
        print(f'{datetime.now()} : No Appointment found')
    else:
        print(f'{datetime.now()} : {countOfAppointments} appointments found')
        play_alarm()


def run():
    print('starting...')
    one_hour = 60*60
    schedule.every(5).minutes.do(Job2)
    #schedule.every().day.at("23:30").do(job, one_hour)
    #schedule.every().day.at("06:30").do(job, one_hour)

    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute 


run()