__author__ = 'weez8031'

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, json

class Create_New_Instance(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        fp = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(fp)
        self.driver.implicitly_wait(30)
        self.base_url = self.config['test_ip']
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Create_New_Instance(self):
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
        driver.find_element_by_xpath("//dd/div//a[text()='Instances' and @href='/project/instances/']").click()
        driver.find_element_by_xpath("//a[@href='/project/instances/launch']").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.config['test_vm_name'])
        Select(driver.find_element_by_id("id_flavor")).select_by_index(1)
        driver.find_element_by_css_selector("option[value=\"1\"]").click()
        Select(driver.find_element_by_id("id_source_type")).select_by_visible_text("Boot from image")
        driver.find_element_by_css_selector("option[value=\"image_id\"]").click()
        Select(driver.find_element_by_id("id_image_id")).select_by_index(1)
        driver.find_element_by_xpath("//ul[@role='tablist']//a[text()='Networking']").click()
        select_network = driver.find_element_by_xpath("//ul[@id='selected_network']").text
        if select_network == '':
            driver.find_element_by_xpath("//ul[@id='available_network']/li[1]/a[1]").click()

        driver.find_element_by_xpath("//input[@value='Launch']").click()

        Success_alert = driver.find_element_by_xpath("//p[contains(text(), 'Launched instance')]")

        if "Success" in Success_alert.text and self.config['test_vm_name'] in str(Success_alert.text):
             print Success_alert.text
        else:
            raise
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_vm_name'] + "')]/td[contains(text(), 'Running')]")

        table_element = driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_vm_name'] + "')]")
        print table_element.text
        table_element.find_element_by_xpath(".//input[@type='checkbox']").click()
        driver.find_element_by_xpath("//button[contains(., 'Terminate Instances')]").click()
        driver.find_element_by_xpath("//a[contains(text(), 'Terminate Instance')]").click()
        terminate_status = driver.find_element_by_xpath("//p[contains(text(), 'Scheduled termination of Instance:')]")
        print terminate_status.text
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
