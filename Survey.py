import logging

from utils import move_file, rename_file, replace, split_filepath


class Survey():
    def __init__(self, cfg):
        if "id" in cfg:
            self._id = cfg["id"]
            logging.debug("Loaded survey id")
        else:
            logging.error(
                "Survey id missing from 'surveys' object in "
                "survey_config.json")
            self._id = None
        if "save_dir" in cfg:
            self._save_dir = cfg["save_dir"]
            logging.debug("Loaded save directory")
        else:
            logging.warn(
                "No save directory (key: 'save_dir') specified in 'surveys' "
                "object in survey_config.json. Default will be used without "
                "error"
            )
            self._save_dir = None
        if "rename" in cfg:
            self._rename = cfg["rename"]
            logging.debug("Loaded file rename")
        else:
            logging.warn(
                "No file rename (key: 'rename') specified in 'surveys' object "
                "in survey_config.json. File will not be renamed."
            )
            self._rename = None

    def getURL(self, url) -> str:
        return url + '/' + self._id

    def getRename(self) -> list[object]:
        return self._rename

    def getSaveDir(self) -> str:
        return self._save_dir

    def rename(self, file_name, downloads_dir):
        new_name = split_filepath(file_name)[1]
        logging.debug(f"Renaming {new_name} file")
        for r in self.getRename():
            logging.debug(f"Replacing {r['replace_pattern']} in file with "
                          f"{r['replace_with']}")
            new_name = replace(
                new_name, r["replace_pattern"], r["replace_with"])
        file_path = f"{downloads_dir}/{file_name}"
        return rename_file(file_path, new_name)

    def move(self, file_path):
        logging.debug(f"moving {file_path} to save directory")
        move_file(file_path, self.getSaveDir())

    def deepCopy(self):
        logging.debug(f"Creating deep copy of {self}")
        if not self.isValid():
            logging.error(
                f"{self} is not a valid Survey. Can't create deep copy.")
            return None
        cfg = {"id": self._id}
        if self._save_dir:
            cfg["save_dir"] = self._save_dir
        if self._rename:
            cfg["rename"] = self._rename
        logging.debug(f"Creating new survey with config: {cfg}")
        newSurvey = Survey(cfg)
        logging.debug(f"New survey created: "
                      f"{newSurvey}. IsValid: {newSurvey.isValid()}")
        return newSurvey

    def isValid(self):
        if self._id:
            return True
        else:
            return False
