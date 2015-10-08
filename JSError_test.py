__author__ = 'weez8031'

#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fp = webdriver.FirefoxProfile()
fp.add_extension(extension='JSErrorCollector.xpi')
driver = webdriver.Firefox(fp)
driver.get("https://codex.wordpress.org/Using_Your_Browser_to_Diagnose_JavaScript_Errors")
driver.get("http://www.webreference.com/programming/javascript/rg31/index.html")
error = driver.execute_script("return window.JSErrorCollector_errors.pump()")
print(len(error))
print error
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found" not in driver.page_source
driver.close()