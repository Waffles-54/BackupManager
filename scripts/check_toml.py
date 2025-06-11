import os
import sys
import tomllib

class TOMLValidator:
    def __init__(self):
        self.SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "backup_manager", "config", "settings.toml")
        self.REQUIRED_STRUCTURE = {
            "general": {
                "doSyncSystem": bool,
                "doDailyUpdates": bool,
                "doWeeklyUpdates": bool,
                "doMonthlyUpdate": bool,
                "doYearlyUpdates": bool,
            },
            "paths": {
                "backupLocation": str,
                "syncPaths": list,
                "backupPaths": list,
            },
            "limits": {
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

    def check_toml(self):
        ###################################################
        # Try to open the toml file and load its contents #
        ###################################################
        try:
            with open(self.SETTINGS_PATH, "rb") as f:
                settings = tomllib.load(f)
        except FileNotFoundError:
            print(f"[ERROR] settings.toml not found at {self.SETTINGS_PATH}")
            sys.exit(1)
        except tomllib.TOMLDecodeError as e:
            print(f"[ERROR] Failed to parse TOML: {e}")
            sys.exit(1)

        missing = []
        type_errors = []
        general_errors = []

        ###########################
        # Validate toml structure #
        ########################### 
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

        if missing or type_errors:
            if missing:
                print(f"[ERROR] Missing required keys:\n - " + "\n - ".join(missing))
            if type_errors:
                print(f"[ERROR] Type errors:\n - " + "\n - ".join(type_errors))
            sys.exit(1)

        ####################
        #  Validate paths  #
        ####################
        if not os.path.isdir(settings["paths"]["backupLocation"]):
            general_errors.append(f"[ERROR] Unable to open backupLocation")

        for value in settings["paths"]["syncPaths"]:
            if not os.path.isdir(value):
                general_errors.append(f"[ERROR] Unable to open syncPath: {value}")

        for value in settings["paths"]["backupPaths"]:
            if not os.path.isdir(value):
                general_errors.append(f"[ERROR] Unable to open backupPath: {value}")

        ####################
        ### Limit Checks ###
        ####################
        if settings["limits"]["allowedWeeklyBackups"] not in range(0, 5):
            general_errors.append(f"[ERROR] Value bounding error in allowedWeeklyBackups: should be between (0-4)")

        if settings["limits"]["allowedMonthlyBackups"] not in range(0, 13):
            general_errors.append(f"[ERROR] Value bounding error in allowedMonthlyBackups: should be between (0-12)")

        if settings["limits"]["allowedYearlyBackups"] < 0:
            general_errors.append(f"[ERROR] Value bounding error in allowedYearlyBackups: should be between (0-inf)")

        # Schedule checks
        if settings["schedule"]["dateOfWeekly"] not in range(0, 7):
            general_errors.append(f"[ERROR] Value bounding error in dateOfWeekly: should be between (0-6)")

        if settings["schedule"]["dateOfMonthly"] not in range(1, 29):
            general_errors.append(f"[ERROR] Value bounding error in dateOfMonthly: should be between (1-28)")

        if settings["schedule"]["dateOfYearly"][0] not in range(1, 13):
            general_errors.append(f"[ERROR] Value bounding error in dateOfYearly[0]: should be between (1-12)")

        if settings["schedule"]["dateOfYearly"][1] not in range(1, 29):
            general_errors.append(f"[ERROR] Value bounding error in dateOfYearly[1]: should be between (1-28)")
        
        if general_errors:
            for error in general_errors:
                print(error)
            # sys.exit(1)

        print("[OK] settings.toml has been validated")
        return settings

if __name__ == "__main__":

    validator = TOMLValidator()   # create an instance
    validator.check_toml()         # call instance method correctly
