
import pandas as pd
from RPA.Browser.Playwright import Playwright
from ACME import ACME
from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers

browser = Playwright()
Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"], headless=False)
acme = ACME("https://acme-test.uipath.com", browser)

class TestACME:
    acme = ACME("https://acme-test.uipath.com", browser)

    def test_open_Websie(self):
        # acme = ACME("https://acme-test.uipath.com", browser)
        acme.openWebsite()
        assert isinstance(acme, ACME)

    def test_login(self):
        # acme = ACME("https://acme-test.uipath.com", browser)
        password = "Szczotar93"
        username = "artur.szczotarski@digitalworkforce.com"
        acme.LogIn(username,password)
        ur = browser.get_url()
        assert ur == "https://acme-test.uipath.com/"
    
    def test_Navigate_MonthlyReports(self):
        acme.Navigate_MonthlyReports()
        assert browser.wait_for_elements_state("id=buttonDownload",state=ElementState.visible)==None



# from ACME import ACME
# from RPA.Browser.Playwright import Playwright
# from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers
# browser = Playwright()

# Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"], headless=False)



# def test_login(self):
#     # given
#     url = "https://acme-test.uipath.com"
#     acme = ACME(url,browser)
#     password = "Szczotar93"
#     username = "artur.szczotarski@digitalworkforce.com"

#     # when
#     assert acme.openWebsite()
#     assert acme.LogIn(password,username)
