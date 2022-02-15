from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from bot import helpers

service = Service('./bot/drivers/chromedriver')
service.start()
options = Options()
# options.headless = True
driver = webdriver.Remote(service.service_url, options=options)
wait = WebDriverWait(driver, 60)

search_url = helpers.get_search_url()
driver.get(search_url)

progress_bar_selector = helpers.ProgressBarSelector()
try:
    wait.until(progress_bar_selector)
except TimeoutException:
    pass

helpers.close_cookie_agreement(driver)
available_flights = helpers.select_available_flights(driver)
flights_data = helpers.parse_flight(available_flights)
print(flights_data)

driver.close()
