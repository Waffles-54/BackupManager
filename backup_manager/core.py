import os
import dirsync
import shutil
import logging

class BackupSystem:
    def __init__(self, sysData):
        self.sysData = sysData

    def syncSystem(self, srcList, dest_base, logger):
        # Load Sync directory (syncLocation)
        try:
            os.chdir(dest_base)
        except FileNotFoundError as e:
            raise Exception(f"Unable to open syncLocation: {dest_base}")
        
        # Configure dirsync logger to be silent
        dirsync_logger = logging.getLogger("dirsync")
        dirsync_logger.disabled = True
        
        # Syncronize paths
        for path in srcList:
            logger.info(f"Syncronizing {path}...")
            normalized_path = os.path.basename(os.path.normpath(path))
            if not os.path.isdir(normalized_path):
                os.mkdir(normalized_path)
            dest = os.path.join(dest_base, "Sync", normalized_path)
            dirsync.sync(path, dest, 'sync', purge="True")
            logger.info(f"Syncronization completed for {path}")

    def generateBackups(self, typeCode):
        paths = self.sysData.config["paths"]
        logger = self.sysData.logger
        dateCode = self.sysData.timeNow.strftime("%m-%d")
        # Valdiate backupLocation
        if not os.path.isdir(paths["backupLocation"]):
            raise Exception(f"Backup location is inaccessible: {paths['backupLocation']}")
        os.chdir(paths["backupLocation"])
       
        # Check if the typeCode already exists (Daily, Weekly, Etc) 
        if not os.path.exists(typeCode):
            os.mkdir(typeCode)
            logger.info(f"Created new directory: {typeCode}")
        os.chdir(typeCode)

        # Check if a dateCode has already been established
        if not os.path.exists(dateCode):
            os.mkdir(dateCode)
            logger.info(f"Created new directory: {dateCode}")
        os.chdir(dateCode)
        dest = os.getcwd()

        # Syncronization backup algorithm
        if self.sysData.config["general"]["doSyncBackup"]:
            for dirname in os.listdir(paths["syncLocation"]):
                full_path = os.path.join(paths["syncLocation"], dirname)
                if os.path.isdir(full_path):
                    logger.info(f"Backing up {full_path}")
                    zip_name = f"{typeCode}_{dateCode}_Sync-{dirname}"
                    shutil.make_archive(zip_name, "zip", full_path)

        # Backup paths
        for path in paths["backupPaths"]:
            logger.info(f"Backing up {path} directory...")
            zip_name = f"{typeCode}_{dateCode}_{os.path.basename(os.path.normpath(path))}"
            shutil.make_archive(zip_name, "zip", path)

    def trimBackups(self):
        path = self.sysData.config["paths"]["backupLocation"]
        limits = self.sysData.config["limits"]

        if not os.path.isdir(path):
            raise Exception(f"Unable to open backupLocation {path}")
        os.chdir(path)

        if os.path.exists("Daily"):
            self.trimHelper("Daily", limits["allowedDailyBackups"])

        if os.path.exists("Weekly"):
            self.trimHelper("Weekly", limits["allowedWeeklyBackups"])

        if os.path.exists("Monthly"):
            self.trimHelper("Monthly", limits["allowedMonthlyBackups"])

        if os.path.exists("Yearly"):
            self.trimHelper("Yearly", limits["allowedYearlyBackups"])

    def trimHelper(self, dirCode, limit):
        path = self.sysData.config["paths"]["backupLocation"]
        targetDir = os.path.join(path, dirCode)
        logger = self.sysData.logger
        dirs = [name for name in os.listdir(targetDir)]

        if len(dirs) > limit:
            logger.info(f"{dirCode} backups exceeds the limit of {limit} backups, trimming...")       
            old_dir = min(dirs, key=lambda d: os.path.getmtime(os.path.join(targetDir, d)))
            old_path = os.path.join(path, dirCode, old_dir)
            logger.info(f"removing oldest {dirCode} archive: {old_dir}...")
            shutil.rmtree(old_path)
            logger.info("Done")
        else:
            logger.info(f"{dirCode} backups within {limit} max limit")
