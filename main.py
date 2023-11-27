class Driver():
    def __init__(self):
        self._survey_results = SurveyResults()

    def run(self):
        self._survey_results.run()

Driver().run()