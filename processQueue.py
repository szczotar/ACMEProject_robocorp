from contextlib import nullcontext
from logging import Handler, error, log
from pydoc import plain
from socket import timeout
import sys
from tkinter import BROWSE
from tkinter.filedialog import SaveAs
from RPA.Robocorp.WorkItems import WorkItems, State
from RPA.Robocorp.Vault import Vault
import pandas as pd
from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers
from RPA.HTTP import HTTP

from RPA.Browser.Playwright import Playwright
import datetime
import logging
import logging.handlers
import os
import time
from populateQueue import Navigate_WorkItems
import glob



browser = Playwright(timeout = "10s")
secrets = Vault()
http = HTTP()
Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"])
                            # downloadsPath =r"C:\Users\admin\Downloads")
context =  browser.new_context(acceptDownloads= True, javaScriptEnabled = True, ignoreHTTPSErrors = True,bypassCSP=True)
os.chdir("output")

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

def Navigate_MonthlyReports():
    browser.click("""xpath=//*[@id="dashmenu"]/div[8]/button""")
    browser.click("text=Download Monthly Report")

def Navigate_UploadYearlyReports():
    browser.click("""xpath=//*[@id="dashmenu"]/div[8]/button""")
    browser.click("text=Upload Yearly Report")
def Navigate_Dashboard():
    browser.click("xpath=/html/body/nav/div/div[1]/a")

def Collect_repotsFromYear(TaxID):

    for monthIndex in range(1,13):
        try:
            browser.type_text("id=vendorTaxID", TaxID)
            browser.select_options_by("id=reportYear", SelectAttribute.value, "2021")
            browser.select_options_by("id=reportMonth", SelectAttribute.value, str(monthIndex))                 
            file_name = rf"{os.getcwd()}\report_{TaxID}_{monthIndex}.csv"
            promise = browser.promise_to_wait_for_download(file_name)
            browser.click("id=buttonDownload")
            browser.wait_for(promise)
        except:
            browser.reload()
            continue

def Combine_MonthlyReports(TaxID):
    # Combine all report to one excel file
    # os.chdir(r"C:\Users\admin\Downloads")
    extension = "csv"
    all_reports = [i for i in glob.glob(f"report_{TaxID}_*.{extension}")]
    combined_reports = pd.concat([pd.read_csv(f) for f in all_reports])
    combined_reports.to_excel(f"Yearly-Report-2021-{TaxID}.xlsx", index = False)
    
    # Delet monthly reports from directory
    for file in [i for i in glob.glob(f"report_{TaxID}_*.{extension}")]:
        os.remove(file)

def Upload_YearlyReport(TaxID):
    # try:
    browser.type_text("id=vendorTaxID", TaxID)
    browser.select_options_by("id=reportYear", SelectAttribute.value, "2021")
    promise = browser.promise_to_upload_file(rf"{os.getcwd()}\Yearly-Report-2021-{TaxID}.xlsx")
    browser.click("""xpath = //*[@id="searchForm"]/div[3]/div/label""")
    browser.wait_for(promise)
    browser.click("id=buttonUpload")

    # except:
    #     browser.reload()
    #     continue
 
                  
def minimal_task():
    
    openWebsite()
    LogIn()
    
    queue = WorkItems()
    while True:

        try:
            queue.get_input_work_item()
            payload = queue.get_work_item_payload()
        
            if not payload:
                break
            Navigate_MonthlyReports()
            Collect_repotsFromYear(payload['TaxID'])
            Combine_MonthlyReports(payload['TaxID'])
            Navigate_Dashboard()
            Navigate_UploadYearlyReports()
            Upload_YearlyReport(payload['TaxID'])
            Navigate_Dashboard()

            queue.release_input_work_item(state= State.DONE)

        except:
            False


if __name__ == "__main__":
    minimal_task()
    

