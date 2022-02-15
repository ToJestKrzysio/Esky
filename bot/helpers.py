from selenium.webdriver.common.by import By


def close_cookie_agreement(driver):
    button_cookie_agreement = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div[class$='summary-buttons'] button[size='large']:last-child"
    )
    button_cookie_agreement.click()
