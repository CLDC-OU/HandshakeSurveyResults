import json
import logging
import os
from dotenv import load_dotenv
from selenium import webdriver

from pathlib import Path

from Survey import Survey

class Config():
    def __init__(self) -> None:
        self.env = False
        self._load_env()
        self._load_config()

        if self.isValid():
            logging.info("Loaded config from survey_config.json")
        else:
            logging.error("Could not load config from survey_config.json. See errors above for reference.")
            return
        
        self._initialize_selenium()

    def getSurveys(self) -> list[Survey]:
        return self._surveys
    def getURL(self) -> str:
        return self._url
    def getDownloadsDir(self) -> str:
        return self._downloads_dir
    def getWebdriver(self) -> webdriver.Chrome:
        return self._webdriver

    def _load_config(self):
        self._chromedriver_path = None
        self._downloads_dir = None
        self._url = None
        self._surveys = None

        cfg = None
        try:
            with open('survey_config.json') as json_file:
                cfg = json.load(json_file)
            logging.info("Survey config loaded")
        except:
            logging.error(f"Could not find survey_config.json")
            return
        
        if "chromedriver_path" in cfg:
            self._chromedriver_path = cfg["chromedriver_path"]
            logging.debug(f"Chromedriver Path loaded from survey_config.json as {self._chromedriver_path}")
        else:
            logging.error("No Chromedriver path (key: 'chromedriver_path') specified in survey_config.json")
        if "handshake_url" in cfg:
            self._url = f'{cfg["handshake_url"]}/edu/surveys'
            logging.debug(f"Handshake URL loaded from survey_config.json as {self._url}")
        else:
            logging.error("No Handshake URL (key: 'handshake_url') specified in survey_config.json")
        if "downloads_dir" in cfg:
            self._downloads_dir = cfg["downloads_dir"]
            logging.debug(f"Downloads directory loaded from survey_config.json as {self._downloads_dir}")
        else:
            logging.warn("No downloads directory (key: 'downloads_dir') specified in survey_config.json. Trying to use Windows default. This may cause unexpected behavior.")
            self._downloads_dir = str(Path.home() / "Downloads")
            logging.debug(f"Downloads directory loaded from Path as {self._downloads_dir}")
        if "surveys" in cfg:
            self._load_surveys(cfg["surveys"])
            if len(self._surveys) < 1:
                logging.error("No valid surveys exist in survey_config.json (key exists, but no valid reports were found)")
                self._surveys = None
            else:
                logging.debug(f"{len(self._surveys)} Survey(s) loaded from survey_config.json")
        else:
            logging.error("No surveys (key: 'surveys') specified in survey_config.json")
    
    def _load_env(self):
        if load_dotenv():
            logging.info(f"Environmental variables successfully loaded")
            self.env = True
        else:
            logging.error(f"There was an error loading the environmental variables. Check that the path variables are correct and the .env file exists")

    def _load_surveys(self, surveys):
        self._surveys = []
        for survey_cfg in surveys:
            logging.debug(f"Loading survey from {survey_cfg}")
            s = Survey(survey_cfg)
            logging.debug(f"Survey: {str(s)}")
            if s.isValid():
                logging.debug(f"Survey {s._id} is valid")
                self._surveys.append(s.deepCopy())
                logging.info(f"Added survey {s._id}")

    def get_username(self):
        if self.env:
            return os.getenv("HS_USERNAME")
    def get_password(self):
        if self.env:
            return os.getenv("HS_PASSWORD")
    def is_institutional(self):
        if self.env:
            return os.getenv("INSTITUTIONAL_EMAIL") == "TRUE"
        
    def _initialize_selenium(self):
        logging.debug("Initializing Selenium...")
        # Set PATH environmental variable to chromedriver-win64
        os.environ["PATH"] += self._chromedriver_path
        logging.debug("Added environmental Path")

        chrome_options = webdriver.ChromeOptions()
        args = ["--start-minimized", "--headless=new", "--disable-popup-blocking"]
        # args = ["--disable-popup-blocking"]
        for arg in args:
            chrome_options.add_argument(arg)
        # Create a new instance of the Chrome driver
        self._webdriver = webdriver.Chrome(options=chrome_options)
        
        logging.debug(f"Initialized new Chrome webdriver instance with the following arguments: [{', '.join(args)}]")
        logging.info("Chrome webdriver initialized")


    def isValid(self):
        return self._chromedriver_path and self._downloads_dir and self._url and self._surveys
    
        