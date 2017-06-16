from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

__all__ = ['Slack']


class Slack:
    _url_template = 'https://{team_name}.slack.com'

    def __init__(self, team_name: str, headless: bool = True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        self._logged_in = False
        self._driver = webdriver.Chrome(chrome_options=options)
        self._url_prefix = Slack._url_template.format(team_name=team_name)

    def login(self, username: str, password: str):
        driver = self._driver

        driver.get(self._url_prefix)
        e = driver.switch_to.active_element
        e.send_keys(username)
        e.send_keys(Keys.TAB)
        e = driver.switch_to.active_element
        e.send_keys(password)
        e.send_keys(Keys.ENTER)

        self._logged_in = driver.current_url != self._url_prefix
        return self._logged_in

    def register_emoji(self, name: str, image_path: str):
        import os
        if not self._logged_in:
            raise RuntimeError('Not logged in')  # TODO: use User-defined Exception
        driver = self._driver

        driver.get(self._url_prefix + '/customize/emoji')
        driver.find_element_by_id('emojiname').send_keys(name)
        img_path = os.path.abspath(image_path)
        driver.find_element_by_id('emojiimg').send_keys(img_path)

        driver.find_element_by_id('emojiname').send_keys(Keys.ENTER)  # Submit

        # Error Handling
        alerts = driver.find_elements_by_css_selector('p.alert.alert_error')
        if len(alerts) > 0:
            raise RuntimeError(' | '.join(a.text for a in alerts))  # TODO: use User-defined Exception

    def quit(self):
        self._driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
