__author__ = 'weez8031'

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, json

class Cinder_Snapshot(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        fp = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(fp)
        self.driver.implicitly_wait(30)
        self.base_url = self.config['test_ip']
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Cinder_Snapshot(self):
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
        driver.find_element_by_xpath("//dd/div//a[text()='Volumes' and @href='/project/volumes/']").click()
        volumes_status = driver.find_element_by_xpath("//ul[@id='volumes_and_snapshots']//li[contains(., 'Volumes')]").get_attribute('class')
        if volumes_status != 'active':
            driver.find_element_by_xpath("//ul[@id='volumes_and_snapshots']//li[contains(., 'Volumes')]").click()
        driver.find_element_by_xpath("//a[@href='/project/volumes/create/']").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.config['test_volume'])
        Select(driver.find_element_by_id("id_volume_source_type")).select_by_visible_text("No source, empty volume")
        driver.find_element_by_xpath("//input[@type='submit' and @value='Create Volume']").click()

        Success_alert = driver.find_element_by_xpath("//p[contains(text(), 'Creating volume')]")

        if "Info:" in Success_alert.text and self.config['test_volume'] in str(Success_alert.text):
             print Success_alert.text
        else:
            raise
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_volume'] + "')]/td[contains(text(), 'Available')]")

        #Create cinder snapshot
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_volume'] + "')]//a[@data-toggle='dropdown']").click()
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_volume'] + "')]//a[contains(. , 'Create Snapshot')]").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(self.config['test_cinder_snapshot'])
        driver.find_element_by_xpath("//input[@type='submit' and @value='Create Volume Snapshot']").click()
        Success_alert = driver.find_element_by_xpath("//p[contains(text(), 'Creating volume snapshot ')]")
        if "Info:" in Success_alert.text and self.config['test_cinder_snapshot'] in str(Success_alert.text):
             print Success_alert.text
        else:
            raise
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_cinder_snapshot'] + "')]/td[contains(text(), 'Available')]")
        #Delete Cinder Snapshot
        driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_cinder_snapshot'] + "')]//input[@type='checkbox']").click()
        driver.find_element_by_xpath("//button[contains(., 'Delete Volume Snapshots')]").click()
        driver.find_element_by_xpath("//a[contains(text(), 'Delete Volume Snapshots')]").click()
        terminate_status = driver.find_element_by_xpath("//p[contains(text(), 'Scheduled deletion of Volume Snapshot:')]")
        print terminate_status.text
        # driver.find_element_by_xpath("//ul[@id='volumes_and_snapshots']//a[contains(., 'Volumes')]").click()
        #naive solution, need this interval because the snapshot is still deleting.
        driver.get(driver.current_url + "?tab=volumes_and_snapshots__volumes_tab")
        time.sleep(10)
        table_element = driver.find_element_by_xpath("//tr[contains(@data-display, '" + self.config['test_volume'] + "')]")
        print table_element.text
        table_element.find_element_by_xpath(".//input[@type='checkbox']").click()
        driver.find_element_by_xpath("//button[contains(., 'Delete Volumes')]").click()
        driver.find_element_by_xpath("//a[contains(text(), 'Delete Volumes')]").click()
        terminate_status = driver.find_element_by_xpath("//p[contains(text(), 'Scheduled deletion of Volume:')]")
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
