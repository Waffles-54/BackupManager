"""
Entry point for backup_manager package.

Allows running the package as a module with:
    python -m backup_manager
"""

import sys

# from .prep import PrepSystem # Not in use right now (Future scaling)
from core import BackupSystem as backup_system
from prep import PrepSystem as prep_system
# from backup_manager.validators.toml_validator import validate_toml_config
# from backup_manager.validators.dep_validator import check_dependencies

def main():
    # Prep datetime    
    sysData = prep_system()
    logger = sysData.logger
    config = sysData.config
    backManager = backup_system(sysData)
    # Heart of the program, Entry point for execution of the package
    try:
        if config["general"]["doSyncSystem"]:
            backManager.syncSystem(config["paths"]["syncPaths"], config["paths"]["syncLocation"], logger)
        if config["general"]["doDailyBackups"]:            
            backManager.generateBackups("Daily")
        if config["general"]["doWeeklyBackups"] and sysData.thisDay == config["schedule"]["dateOfWeekly"]:
            backManager.generateBackups("Weekly")
        if config["general"]["doMonthlyBackups"] and sysData.thisDay == config["schedule"]["dateOfMonthly"]:
            backManager.generateBackups("Monthly")
        if config["general"]["doYearlyBackups"] and sysData.thisMonth == config["schedule"]["dateOfYearly"][0] and sysData.thisDay == config["schedule"]["dateOfYearly"][1]:
            backManager.generateBackups("Yearly")
        backManager.trimBackups()
    except Exception as e:
        logger.error(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
