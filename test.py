# -*- coding=utf-8 -*

from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='./chromedriver')


driver.get('https://www.baidu.com')
driver.maximize_window()

driver.find_element_by_id("kw").send_keys('python')
a = driver.find_element_by_xpath('//*[@id="su"]').get_attribute('velue')
print(a)
driver.find_element_by_xpath('//*[@id="su"]').click()
time.sleep(1)
driver.save_screenshot('a.png')
print(driver.page_source)

