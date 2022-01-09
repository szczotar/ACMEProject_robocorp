"""Template robot with Python."""


from re import T
from RPA.Browser import Browser
from RPA.Robocorp.WorkItems import WorkItems, State
from RPA.Robocorp.Vault import Vault
import pandas as pd
from Browser import Browser, SupportedBrowsers
import time
from RPA.HTTP import HTTP

import requests
from bs4 import BeautifulSoup

# a = pd.DataFrame(data = {"Name":["Arutr","Dawid"], "Age":["29","30"]})
# print(a)

browser = Browser()
secrets = Vault()
http = HTTP()

Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"], headless = False)


def openWebsite():
    app_url = secrets.get_secret("process_website")["url"]
    browser.new_page(app_url)
    # browser.open_browser(app_url)
 
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
            break
    
    WI4Table = DataScraped.loc[DataScraped["Type"] == "WI4"]
    WI4Table = WI4Table.reset_index(drop=True)
    print(WI4Table)
    return WI4Table

def Get_TaxIDs(Table):
    app_url = secrets.get_secret("process_website")["url"]
    queue = WorkItems()
    queue.get_input_work_item()

    for item in Table['WIID']:
        browser.new_page(f'{app_url}/work-items/{item}')
        ItemData = browser.get_text("xpath=/html/body/div/div[2]/div/div[2]/div/div/div[1]/p")
        TaxID = ItemData.split()[1]
        queue.create_output_work_item()
        queue.set_work_item_variable("WIID", item)
        queue.set_work_item_variable("TaxID", TaxID)
        queue.save_work_item()

        print(TaxID)
        time.sleep(2)
        browser.close_page()

        
if __name__ == "__main__":
    openWebsite()
    LogIn()
    Navigate_WorkItems()
    WI4Table = Scrape_Table()
    Get_TaxIDs(WI4Table)
    
