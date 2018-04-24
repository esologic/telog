import os
import yaml
import logging
import logging.config

directory_name, file_name = os.path.split(os.path.abspath(__file__))


def setup_logging(config_file_name="config.yaml", log_files_dir_name="logs", default_level=logging.INFO):

    print("Setting up text logs")

    config_file_path = os.path.join(directory_name, config_file_name)
    print("Loading in config file [" + str(config_file_path) + "]")

    log_file_directory = os.path.join(directory_name, log_files_dir_name)
    print("Storing logs in directory [" + str(log_file_directory) + "]")

    if not os.path.exists(log_file_directory):
        print("Had to create [" + str(log_file_directory) + "]")
        os.makedirs(log_file_directory)

    log_file_path = os.path.join(log_file_directory, "logs.txt")
    print("Storing logs in file [" + str(log_file_path) + "]")

    if os.path.exists(config_file_path):
        with open(config_file_path, 'rt') as f:
            try:
                cfg = yaml.safe_load(f.read())
                cfg["handlers"]["file"]["filename"] = log_file_path
                logging.config.dictConfig(cfg)
            except Exception as e:
                print('Error in Logging Configuration. Using default configs', e)
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print("Path doesn't exist", config_file_path)
        print('Failed to load configuration file. Using default configs')

    print("Text logs configured")


class Filter(logging.Filter):

    def __init__(self, filter_name="filter.yaml"):

        self.__name_to_level__ = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARN": logging.WARNING,
                                  "WARNING": logging.WARNING, "ERROR": logging.ERROR}

        self.mode = None
        self.filter_dict = {}

        with open(os.path.join(directory_name, filter_name), 'rt') as f:

            try:
                config_dict = yaml.safe_load(f.read())

                self.mode = config_dict["filter_in"]
                self.filter_dict = config_dict["modules"]

                # do name to level conversion
                for mod in self.filter_dict:

                    if isinstance(self.filter_dict[mod], dict):
                        module_dict = self.filter_dict[mod]

                        for method in module_dict:
                            module_dict[method] = self.name_to_level(module_dict[method])

                    else:
                        self.filter_dict[mod] = self.name_to_level(self.filter_dict[mod])

            except Exception:
                print("There was a problem loading in the [" + str(filter_name) + "] filter")

    def name_to_level(self, name):
        return self.__name_to_level__[name.upper()]

    def filter(self, record):

        if self.mode is False:  # filter out mode

            if record.module in self.filter_dict:
                try:
                    if record.funcName in self.filter_dict[record.module]:
                        if record.levelno <= self.filter_dict[record.module][record.funcName]:
                            return False

                except TypeError: # meaning the whole module is being filtered
                    if record.levelno <= self.filter_dict[record.module]:
                        return False

            return True

        if self.mode is True:  # filter in mode

            if record.module in self.filter_dict:
                try:
                    if record.funcName in self.filter_dict[record.module]:
                        if record.levelno >= self.filter_dict[record.module][record.funcName]:
                            return True

                except TypeError:  # meaning the whole module is being filtered
                    if record.levelno >= self.filter_dict[record.module]:
                        return True

            return False


        else:
            return True # the filter config file was bad, pass all messages


setup_logging()

telogger = logging.getLogger(__name__)

telogger.addFilter(Filter())

