"""Template robot with Python."""


from logging import Handler, error, log
import sys
from tkinter import BROWSE
from RPA.Robocorp.WorkItems import WorkItems, State
from RPA.Robocorp.Vault import Vault
import pandas as pd
from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers

from RPA.Browser.Playwright import Playwright
import datetime
import logging
import logging.handlers
import os

import time
from RPA.HTTP import HTTP
import requests
from bs4 import BeautifulSoup
os.chdir("output")

# handler = logging.handlers.WatchedFileHandler(
#     os.environ.get("LOGFILE", r"C:\Users\admin\Desktop\Robocorp\ACME_Project\output\stdout.log"))
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root = logging.getLogger()
# root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
# root.addHandler(handler)

logging.basicConfig(filename=f"{os.getcwd()}/logs.log",level=logging.INFO)

browser = Playwright()
secrets = Vault()
http = HTTP()
Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"])

def openWebsite():
    try:
        app_url = secrets.get_secret("process_website")["url"]
        browser.new_page(app_url)
        logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " login success")    
    except:
        print(error)
    
def LogIn():
    Username = secrets.get_secret("credentials")["username"]
    Password = secrets.get_secret("credentials")["password"]
    browser.type_text("id=email", Username)
    browser.type_text("id=password",Password)
    browser.click("xpath=/html/body/div/div[2]/div/div/div/form/button")

def Navigate_WorkItems():
    browser.click("""xpath=//*[@id="dashmenu"]/div[2]/a/button""")
    time.sleep(3)

def Scrape_Table():
    DataScraped = pd.DataFrame()
    while True:
        try:
            tableHTML = browser.get_property("xpath =/html/body/div/div[2]/div/table", "outerHTML")
            single_table = pd.read_html(tableHTML)
            DataScraped = pd.concat([DataScraped, single_table[0]])
            browser.click("text=>")

        except (AssertionError) as err:
             logging.error(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " no more pages")
             break
  
    WI4Table = DataScraped.loc[DataScraped["Type"] == "WI4"]
    WI4Table = WI4Table.reset_index(drop=True)
    return WI4Table

def Get_TaxIDs(Table):
    app_url = secrets.get_secret("process_website")["url"]
    queue = WorkItems()
    queue.get_input_work_item()

    for item in Table['WIID']:
        try:
            browser.new_page(f'{app_url}/work-items/{item}')
            ItemData = browser.get_text("xpath=/html/body/div/div[2]/div/div[2]/div/div/div[1]/p")
            TaxID = ItemData.split()[1]
            queue.create_output_work_item()
            queue.set_work_item_variable("WIID", item)
            queue.set_work_item_variable("TaxID", TaxID)
            queue.save_work_item()
        except:
            browser.close_page()
            continue
        finally:
            browser.close_page()

def main():
    try:
        openWebsite()
        LogIn()
        Navigate_WorkItems()
        WI4Table = Scrape_Table()
        Get_TaxIDs(WI4Table)

    finally:
        browser.close_page()

if __name__ == "__main__":
    main()
