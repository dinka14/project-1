import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select


class SelectResults(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                       desired_capabilities=DesiredCapabilities.CHROME)

    def test_select(self):
        driver = self.driver
        driver.get("https://career.luxoft.com/job-opportunities/")
        try:
            driver.set_page_load_timeout(5)
        except TimeoutException:
            pass
        Select(driver.find_element_by_id("search_type")).select_by_value("118283")
        search = driver.find_element_by_name("arrFilter_ff[NAME]")
        search.clear()
        search.send_keys("AAAAAAA")
        driver.find_element_by_xpath("//button[@type='submit'][contains(text(),'Search')]").click()
        message = driver.find_element_by_xpath("//h1[@class='h-xmd'][contains(text(),'Sorry, No Records Found:(')]").text
        self.assertTrue("SORRY", str(message))

    def tearDown(self):
        self.driver.close()
