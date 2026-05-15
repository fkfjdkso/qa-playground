import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    country = (By.CSS_SELECTOR, "#country_input")
    zip_code = (By.CSS_SELECTOR, "#zip_input")
    city = (By.CSS_SELECTOR, "#city_output")
    save_button = (By.XPATH, '//*[@id="submit_btn"]')
    save_status = (By.CSS_SELECTOR, "#status_message")

    # баг панель
    slow_db_checkbox = (By.XPATH, '//*[@id="bug_slow_db"]')
    duplicates_checkbox = (By.XPATH, '//*[@id="bug_integrity"]')
    ghost_button_checkbox = (By.XPATH, '//*[@id="bug_ui_ghost"]')
    data_truncation_checkbox = (By.XPATH, '//*[@id="bug_data_loss"]')

    def find(self, *args):
        return self.driver.find_element(*args)

    def _wait_for_status_text(self, expected_text: str, timeout: int):
        wait = WebDriverWait(self.driver, timeout) if timeout != 10 else self.wait
        wait.until(EC.text_to_be_present_in_element(self.save_status, expected_text))
        return self.find(*self.save_status).text

    @allure.step("Заполнение формы: страна - {country}, zip - {zip}")
    def fill_form(self, country: str, zip: str):
        self.find(*self.country).send_keys(country)
        zip_elem = self.find(*self.zip_code)
        zip_elem.send_keys(zip)
        self.driver.execute_script("arguments[0].blur();", zip_elem)

    @allure.step("Нажатие кнопки Save")
    def click_save(self):
        self.find(*self.save_button).click()

    @allure.step("Ожидание и получения сообщения об успехе")
    def get_status(self, expected="Saved", timeout=10):
        return self._wait_for_status_text(expected, timeout)

    @allure.step("Ожидание и получение названия города")
    def city_detect(self):
        placeholders = ["Waiting for API...", "Loading...", ""]
        self.wait.until(
            lambda driver: driver.find_element(*self.city).get_attribute("value")
            not in placeholders
        )
        return self.find(*self.city).get_attribute("value")

    @allure.step("Включение бага {bug_name}")
    def toggle_bug(self, bug_name: str):
        locator_name = f"{bug_name}_checkbox"
        locator = getattr(self, locator_name, None)
        if locator:
            self.find(*locator).click()
