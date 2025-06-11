"""
Entry point for backup_manager package.

Allows running the package as a module with:
    python -m backup_manager
"""

import datetime
import sys

# from .prep import PrepSystem # Not in use right now (Future scaling)
from .core import BackupSystem

def main(logger, settings=None, argv=None):
    # Prep datetime
    timeNow = datetime.datetime.today()
    today = timeNow.weekday()

    # This package should be loaded externally
    if settings is None:
        logger.critical("Settings must be passed in explicitly")
        sys.exit(1)
    if argv is None:
        argv = sys.argv[1:]
    # Setup logging config here or import logging_config if you have one
    
    # Initialize prep and core systems
    # Future work #TODO
    # prep = PrepSystem()
    # if not prep.conf_check():
    #     logging.error("Configuration validation failed. Exiting.")
    #     sys.exit(1)
    # prep.arg_parser("")  # parse command-line args if needed

    # Heart of the program, Entry point for execution of the package
    backup = BackupSystem()
    if settings["general"]["doSyncSystem"]:
        backup.syncSystem(settings["paths"]["syncPaths"], settings["paths"]["backupLocation"], logger)
    if settings["general"]["doDailyUpdates"]:
        dateCode = datetime.datetime.now().strftime("%m-%d")
        backup.generateBackups("Daily", settings["general"]["doSyncBackup"], settings["paths"], dateCode, logger)
    if settings["general"]["doWeeklyUpdates"] and today == settings["schedule"]["dateOfWeekly"]:
        dateCode = datetime.datetime.now().strftime("%m-%d")
        backup.generateBackups("Weekly", settings["general"]["doSyncBackup"], settings["paths"], dateCode, logger)
    if settings["general"]["doMonthlyUpdates"] and today == settings["schedule"]["dateOfMonthly"]:
        dateCode = datetime.datetime.now().strftime("%m")
        backup.generateBackups("Monthly", settings["general"]["doSyncBackup"], settings["paths"], dateCode, logger)

    # if settings["general"]["doYearlyUpdates"] and today == settings["schedule"]["dateOfYearly"]:
    #     dateCode_daily = datetime.datetime.now().strftime("%Y")
        # backup.generateBackups("Y", settings["paths"])
    # backup.bac_trimmer()

if __name__ == "__main__":
    main()
