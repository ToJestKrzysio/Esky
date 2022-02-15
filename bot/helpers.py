from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def close_cookie_agreement(driver: WebDriver) -> None:
    """
    Closes cookie pop-up on the site.
    """
    button_cookie_agreement = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div[class$='summary-buttons'] button[size='large']:last-child"
    )
    button_cookie_agreement.click()


def get_search_url() -> str:
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

    return (f"https://www.esky.pl/flights/select/{trip_type}/{departure_airport_type}/{departure}/"
            f"{arrival_airport_type}/{arrival}?departureDate={departure_date}&returnDate={return_date}"
            f"&pa={pax_adult}&py={pax_young}&pc={pax_children}&pi={pax_infant}&sc={flight_standard}")


def select_available_flights(driver: WebDriver) -> list[WebElement]:
    flights = driver.find_elements(
        by=By.CLASS_NAME,
        value="flight-content"
    )
    return flights


def parse_flight(flights: list[WebElement]) -> list:
    flights_data = []
    for flight in flights:
        flights_data.append(flight.find_element(By.CLASS_NAME, "amount").text)
    return flights_data


class ProgressBarSelector:

    def __init__(self):
        self.value = True

    def __call__(self, driver: WebDriver) -> bool:
        progress_bar = driver.find_element(
            by=By.CSS_SELECTOR,
            value="div progress-bar"
        )
        current_value = bool(progress_bar.text)
        is_completed = not (current_value or self.value)
        self.value = current_value
        return is_completed
