import logging
import os
import time
from Config import Config
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SurveyResults():
    def __init__(self):
        self._config = Config()

    def run(self):
        if self._config.isValid() is False:
            logging.error("Invalid or incomplete config provided. Terminating execution.")
            return
        print(self._config.getSurveys())
        for survey in self._config.getSurveys():
            logging.debug(f"Loading survey " + survey._id)
            self._config.getWebdriver().get(survey.getURL(self._config.getURL()))
            self._wait = WebDriverWait(self._config.getWebdriver(), 10)
            if self._config.is_institutional():
                self._sso_login()
            else:
                self._non_sso_login()
            self._download_survey()
            downloaded_survey = self._get_download().pop()
            if not downloaded_survey:
                break
            file_loc = survey.rename(downloaded_survey, self._config.getDownloadsDir())
            survey.move(file_loc)
        self._quit()
        
    def _quit(self):
        self._config.getWebdriver().quit()

    def _sso_login(self):
        self._get_sso_login_btn().click()
        logging.debug('Navigated to login page')
        username_field = self._config._webdriver.find_element(
            (By.ID, 'username')
        )
        username_field.send_keys(self._config.get_username())
        username_field.send_keys(Keys.TAB)
        username_field.send_keys(self._config.get_password())
        username_field.send_keys(Keys.RETURN)

    def _non_sso_login(self):
        self._get_non_sso_login_btn().click()
        logging.debug('Navigated to login page')

        self._wait.until(
            EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Next')]")
            )
        )
        username_field = self._config.getWebdriver().find_element(By.ID, 'non-sso-email-address')
        username_field.send_keys(self._config.get_username())
        username_field.send_keys(Keys.RETURN)

        self._get_non_sso_continue_btn().click()
        self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'Current Student')]")
            )
        )

        password_field = self._config.getWebdriver().find_element(By.ID, 'password')
        password_field.send_keys(os.getenv('HS_PASSWORD'))

        logging.debug('Entered login information')
        password_field.send_keys(Keys.RETURN)

        self._wait.until(EC.url_contains('edu'))
        logging.debug('Logged in')
    
    def _get_sso_login_btn(self) -> WebElement:
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "sso-button")
            )
        )
    def _get_non_sso_login_btn(self) -> WebElement:

        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'sign in with your email address')]")
            )
        )
    def _get_non_sso_continue_btn(self) -> WebElement:
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'log in using your Handshake credentials')]")
            )
        )
    
    def _get_download_btn(self) -> WebElement:
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'Download Results (CSV)')]")
            )
        )

    def _get_download_ready_btn(self) -> WebElement:
        self._wait = WebDriverWait(self._config.getWebdriver(), 180)
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'Your download is ready. Click here to retrieve the file.')]")
            )
        )

    def _download_survey(self):
        self._get_download_btn().click()
        logging.debug('Survey page loaded, download button clicked.')

        logging.debug('Waiting for download to be ready...')
        
        self._get_download_ready_btn().click()
        logging.debug('Download prepared! downloading...')

    def _get_download(self):
        # Wait for the download to finish

        max_wait_time = 120
        initial_files = set(os.listdir(self._config.getDownloadsDir()))

        # Periodically check the downloads directory for new files
        start_time = time.time()
        new_files = False
        while time.time() - start_time < max_wait_time:
            current_files = set(os.listdir(self._config.getDownloadsDir()))

            # Check if there are any new files
            new_files = current_files - initial_files
            if new_files:
                break

            time.sleep(1)  # Wait for 1 second before checking again

        if new_files:
            logging.debug(f"Successfully downloaded {new_files}")
            return new_files
        else:
            logging.error("Download timed out.")
            return None