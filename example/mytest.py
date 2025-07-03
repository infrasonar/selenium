from infrasonar_selenium import TestBase
from selenium import webdriver
from selenium.webdriver.common.by import By


class MyTest(TestBase):

    description = 'Example test'
    url = 'https://www.selenium.dev/selenium/web/web-form.html'
    version = 'v0'

    @classmethod
    def test(cls, driver: webdriver.Remote):
        title = driver.title
        assert title == "Web form"

        driver.implicitly_wait(0.5)

        text_box = driver.find_element(by=By.NAME, value="my-text")
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

        text_box.send_keys("Selenium")
        submit_button.click()

        message = driver.find_element(by=By.ID, value="message")
        value = message.text

        assert value == "Received!"


export = MyTest

if __name__ == '__main__':
    MyTest().print_run()  # Prints the output
