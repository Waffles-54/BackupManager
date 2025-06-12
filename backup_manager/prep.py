import logging
import os
import datetime
try:
    import tomllib 
except ModuleNotFoundError:
    import tomli as tomllib
from logging import FileHandler
from datetime import datetime

class PrepSystem:
    def __init__(self):
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.toml")
        self.REQUIRED_STRUCTURE = {
            "general": {
                "doSyncSystem": bool,
                "doSyncBackup": bool,
                "doDailyBackups": bool,
                "doWeeklyBackups": bool,
                "doMonthlyBackups": bool,
                "doYearlyBackups": bool,
            },
            "paths": {
                "backupLocation": str,
                "syncLocation": str,
                "syncPaths": list,
                "backupPaths": list,
            },
            "limits": {
                "allowedDailyBackups": int,
                "allowedWeeklyBackups": int,
                "allowedMonthlyBackups": int,
                "allowedYearlyBackups": int,
            },
            "schedule": {
                "dateOfWeekly": int,
                "dateOfMonthly": int,
                "dateOfYearly": list,
            }
        }

        self.timeNow = datetime.now()
        self.thisDay = self.timeNow.day
        self.thisMonth = self.timeNow.month

        # Generate logs directory and prepare a session log
        LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(LOG_DIR, exist_ok=True)
        DATE = datetime.now().strftime("%Y-%m-%d")
        LOG_PATH = os.path.join(LOG_DIR, f"{DATE}_Backup-Manager.log")
        LOG_FILEPATH = os.path.basename(LOG_PATH)
        logger = logging.getLogger(LOG_FILEPATH)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")

        # Regular file handler
        file_handler = FileHandler(LOG_PATH, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Console output setup
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        self.logger = logger

        # TOML Loading / Validation
        logger.info("Starting TOML Validation...")
        try:
            with open(self.CONFIG_PATH, "rb") as f:
                settings = tomllib.load(f)
        except FileNotFoundError:
            logger.exception("Errors in config.toml, see log file for more information")
        except tomllib.TOMLDecodeError as e:
            logger.exception(f"Failed to parse TOML: {e}")

        missing = []
        type_errors = []
        general_errors = []

        # Validate toml structure
        for section, keys in self.REQUIRED_STRUCTURE.items():
            if section not in settings:
                missing.append(f"[{section}] (entire section missing)")
                continue

            for key, expected_type in keys.items():
                if key not in settings[section]:
                    missing.append(f"{section}.{key}")
                    continue

                value = settings[section][key]
                # type check: allow list of int/str (special case)
                if expected_type == list and not isinstance(value, list):
                    type_errors.append(f"{section}.{key} is {type(value).__name__}, expected list")
                elif expected_type != list and not isinstance(value, expected_type):
                    type_errors.append(f"{section}.{key} is {type(value).__name__}, expected {expected_type.__name__}")

        # Report errors to the logger and throw an error
        if missing or type_errors:
            if missing:
                logger.error(f"Missing required keys:\n - " + "\n - ".join(missing))
            if type_errors:
                logger.error(f"Type errors:\n - " + "\n - ".join(type_errors))
            raise Exception("Errors in config.toml, see log file for more information")

        # Configuration validation for sync system
        if settings["general"]["doSyncBackup"]:
            if not os.path.isdir(settings["paths"]["syncLocation"]):
                general_errors.append(f"Unable to access syncLocation")

            # Validate paths for syncronization (if sync sytem in use)
            for value in settings["paths"]["syncPaths"]:
                if not os.path.isdir(value):
                    general_errors.append(f"Unable to access syncPath: {value}")

        #  Validate paths
        if not os.path.isdir(settings["paths"]["backupLocation"]):
            general_errors.append(f"Unable to access backupLocation")

        # Validate backup paths
        for value in settings["paths"]["backupPaths"]:
            if not os.path.isdir(value):
                general_errors.append(f"Unable to access backupPath: {value}")

        # Limit Checks [x, y)
        if settings["limits"]["allowedDailyBackups"] not in range(0, 8):
            general_errors.append(f"Value bounding error in allowedDailyBackups: should be between (0-7)")
            
        if settings["limits"]["allowedWeeklyBackups"] not in range(0, 5):
            general_errors.append(f"Value bounding error in allowedWeeklyBackups: should be between (0-4)")

        if settings["limits"]["allowedMonthlyBackups"] not in range(0, 13):
            general_errors.append(f"Value bounding error in allowedMonthlyBackups: should be between (0-12)")

        if settings["limits"]["allowedYearlyBackups"] < 0:
            general_errors.append(f"Value bounding error in allowedYearlyBackups: should be between (0-inf)")

        # Schedule checks [x, y)
        if settings["schedule"]["dateOfWeekly"] not in range(0, 7):
            general_errors.append(f"Value bounding error in dateOfWeekly: should be between (0-6)")

        if settings["schedule"]["dateOfMonthly"] not in range(1, 29):
            general_errors.append(f"Value bounding error in dateOfMonthly: should be between (1-28)")

        if settings["schedule"]["dateOfYearly"][0] not in range(1, 13):
            general_errors.append(f"Value bounding error in dateOfYearly[0]: should be between (1-12)")

        if settings["schedule"]["dateOfYearly"][1] not in range(1, 29):
            general_errors.append(f"Value bounding error in dateOfYearly[1]: should be between (1-28)")
        
        if general_errors:
            for error in general_errors:
                logger.error(error)
            raise Exception("Errors in config.toml, see log file for more information")

        logger.info("settings.toml has been validated")
        self.config = settings

    def arg_parser(self, args):
        pass
