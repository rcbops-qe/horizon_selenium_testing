__author__ = 'weez8031'

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import json

class Delete_Security_Rules(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        fp = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(fp)
        self.driver.implicitly_wait(30)
        self.base_url = self.config['test_ip']
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Delete_Security_Rules(self):
        driver = self.driver
        driver.get(self.base_url + "/auth/login/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.config['user'])
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.config['password'])
        driver.find_element_by_id("loginBtn").click()
        driver.find_element_by_css_selector("dt").click()
        compute_status = driver.find_element_by_xpath("//h4[contains(. , 'Compute')]").get_attribute('class')

        if compute_status != 'active':
            driver.find_element_by_xpath("//dd/div/h4[text()[contains(.,'Compute')]]").click()
        driver.find_element_by_xpath("//dd/div//a[text()='Access & Security' and @href='/project/access_and_security/']").click()
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_security_group'] + "')]//input").click()
        driver.find_element_by_xpath("//button[contains(., 'Delete Security Groups')]").click()
        driver.find_element_by_xpath("//a[contains(text(), 'Delete Security Groups')]").click()


        terminate_status = driver.find_element_by_xpath("//p[contains(text(), 'Deleted Security Group: " + self.config['test_security_group'] + "')]")
        print terminate_status.text
        driver.find_element_by_xpath("//div[@id='profile_editor_switcher']/button").click()
        driver.find_element_by_link_text("Sign Out").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
