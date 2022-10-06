from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import lxml

def driversetup(url,downloadpath,headlessboo):
    ua = UserAgent()
    userA = ua.random

    coptions = webdriver.ChromeOptions()
    coptions.add_argument("--incognito")
    if headlessboo == True:
        coptions.add_argument("--headless")
    coptions.add_argument(f'user-agent={userA}')
    coptions.add_experimental_option("detach", True)
    prefs = {'download.default_directory' : downloadpath}
    coptions.add_experimental_option('prefs', prefs)
    cdver = webdriver.Chrome(options=coptions,service=Service(ChromeDriverManager().install()))
    cdver.get(url)
    return cdver


def click(driver,elem):
    driver.execute_script("arguments[0].click();", elem) 

def selectbox(driver,elem):
    print()