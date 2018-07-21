from selenium import webdriver
url = 'http://www.webscrapingfordatascience.com/complexjavascript/'
# chromedriver should be in the same path as your Python script
driver = webdriver.Chrome()
driver.get(url)
for quote in driver.find_elements_by_class_name('quote'):
    print(quote.text)
input('Press ENTER to close the automated browser')
driver.quit()