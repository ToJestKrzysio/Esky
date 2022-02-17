from __future__ import annotations

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
    trip_type = "roundtrip"
    departure_airport_type = "ap"
    arrival_airport_type = "ap"

    departure = "krk"
    arrival = "dps"

    departure_date = "2022-03-26"
    return_date = "2022-04-02"

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


class FlightDataParser:

    def __init__(self, flight_data: WebElement):
        self.data = flight_data
        self.dict = {"outbound": {}, "return": {}}

    def add_price(self) -> FlightDataParser:
        price = self.data.find_element(By.CLASS_NAME, "amount").text
        self.dict["price"] = int(price.replace(" ", ""))
        return self

    def add_airports(self) -> FlightDataParser:
        outbound_flight, return_flight = self.data.find_elements(By.TAG_NAME, "flight-connections")
        self.dict["outbound"]["airports"] = self._get_airports(outbound_flight)
        self.dict["return"]["airports"] = self._get_airports(return_flight)
        return self

    @staticmethod
    def _get_airports(section: WebElement) -> dict:
        departure = section.find_element(By.CSS_SELECTOR, ".departure-airport span").text
        arrival = section.find_element(By.CSS_SELECTOR, ".arrival-airport span").text
        change_elements = section.find_elements(By.CSS_SELECTOR, ".interchange-inner div span")
        interchanges = tuple(change.get_attribute("innerHTML") for change in change_elements)
        return {
            "departure": departure,
            "interchanges": interchanges,
            "arrival": arrival,
        }

    def add_hours(self) -> FlightDataParser:
        outbound_data, return_data = self.data.find_elements(By.CLASS_NAME, "leg-group-container")
        self.dict["outbound"]["travel_time"] = self._get_hours(outbound_data)
        self.dict["return"]["travel_time"] = self._get_hours(return_data)
        return self

    @staticmethod
    def _get_hours(section: WebElement) -> dict:
        departure = section.find_element(By.CSS_SELECTOR, ".hour.departure").text
        arrival = section.find_element(By.CSS_SELECTOR, ".hour.arrival").text
        travel_time = section.find_element(By.CSS_SELECTOR, ".time").text
        return {
            "departure": departure,
            "arrival": arrival,
            "time": travel_time,
        }

    def value(self) -> dict:
        return self.dict

    def add_operators(self) -> FlightDataParser:
        outbound_data, return_data = self.data.find_elements(By.CLASS_NAME, "main-infos")
        self.dict["outbound"]["operators"] = self._get_operators(outbound_data)
        self.dict["return"]["operators"] = self._get_operators(return_data)
        return self

    @staticmethod
    def _get_operators(section: WebElement) -> tuple:
        operator_elements = section.find_elements(By.CSS_SELECTOR, "img-fallback.logo img")
        operators = tuple(operator.get_attribute("alt") for operator in operator_elements)
        return operators
