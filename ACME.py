

# from RPA.Browser.Playwright import Playwright
# from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers
# from RPA.Robocorp.Vault import Vault
# browser = Playwright()
# secrets = Vault()
# Chrom = browser.new_browser(browser = SupportedBrowsers["chromium"], headless=False)


class ACME:
    def __init__(self, url, browser):
        self.url = url
        self.browser = browser

    def openWebsite(self):
        self.browser.new_page(self.url)

    def LogIn(self,Username,Password):
        self.browser.type_text("id=email", Username)
        self.browser.type_text("id=password",Password)
        self.browser.click("xpath=/html/body/div/div[2]/div/div/div/form/button")

    def Navigate_MonthlyReports(self):
        self.browser.click("""xpath=//*[@id="dashmenu"]/div[8]/button""")
        self.browser.click("text=Download Monthly Report")


