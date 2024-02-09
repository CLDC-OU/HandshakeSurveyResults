from SurveyResults import SurveyResults
from datetime import datetime as dt

import logging
logfile = f"logs/{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(
    filename=logfile,
    encoding='utf-8',
    level=logging.DEBUG,
    filemode='w',
    format='%(levelname)s:%(asctime)s:[%(module)s] %(message)s'
)


class Driver():
    def __init__(self):
        self._survey_results = SurveyResults()

    def run(self):
        self._survey_results.run()


Driver().run()
