from selenium import webdriver

from bot import helpers

trip_type = 'roundtrip'
departure_airport_type = "ap"
arrival_airport_type = "ap"

departure = "krk"
arrival = "lon"

departure_date = "2022-02-26"
return_date = "2022-03-26"

pax_adult = 1
pax_young = 0
pax_children = 0
pax_infant = 0

flight_standard = "economy"

# url = f"https://www.esky.pl/flights/select/roundtrip/ap/krk/ap/barc?departureDate=2022-02-15&returnDate=2022-02-18&pa=1&py=0&pc=0&pi=0&sc=economy"

url = (f"https://www.esky.pl/flights/select/{trip_type}/{departure_airport_type}/{departure}/"
       f"{arrival_airport_type}/{arrival}?departureDate={departure_date}&returnDate={return_date}"
       f"&pa={pax_adult}&py={pax_young}&pc={pax_children}&pi={pax_infant}&sc={flight_standard}")

driver = webdriver.Chrome("./bot/chromedriver")
driver.get(url)

helpers.close_cookie_agreement(driver)
