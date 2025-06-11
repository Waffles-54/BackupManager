import os
import dirsync
import shutil
import logging

class BackupSystem:
    # def __init__(self):
    #     pass

    def syncSystem(self, srcList, dest_base, logger):
        # Configure dirsync logger to be silent
        dirsync_logger = logging.getLogger("dirsync")
        dirsync_logger.disabled = True

        # Load Sync directory (backupLocation)
        try:
            os.chdir(dest_base)
        except FileNotFoundError as e:
            logger.error(f"Unable to open backup path: {dest_base}")
            return
        
        # Load Sync directory
        if not os.path.isdir("Sync"):
            logger.info(f"Sync directory not found, generating directory...")
            os.mkdir("Sync")
            logger.info(f"Sync directory generated")
        os.chdir("Sync")

        # Syncronize paths
        for path in srcList:
            logger.info(f"Syncronizing {path}...")
            normalized_path = os.path.basename(os.path.normpath(path))
            if not os.path.isdir(normalized_path):
                os.mkdir(normalized_path)
            dest = os.path.join(dest_base, "Sync", normalized_path)
            dirsync.sync(path, dest, 'sync', purge="True")
            logger.info(f"Syncronization completed for {path}")

    def generateBackups(self, typeCode, doSyncBack, paths, dateCode, logger):
        # Valdiate backupLocation
        if not os.path.isdir(paths["backupLocation"]):
            logger.error(f"Backup location is inaccessible: {paths['backupLocation']}")
            return
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
        if doSyncBack:
            syncPath = os.path.join(paths["backupLocation"], "Sync")
            for dirname in os.listdir(syncPath):
                full_path = os.path.join(syncPath, dirname)
                if os.path.isdir(full_path):
                    logger.info(f"Backing up {full_path}")
                    zip_name = f"{typeCode}_{dateCode}_Sync-{dirname}"
                    shutil.make_archive(zip_name, "zip", full_path)

        # Backup paths
        for path in paths["backupPaths"]:
            logger.info(f"Backing up {path} directory...")
            zip_name = f"{typeCode}_{dateCode}_{os.path.basename(os.path.normpath(path))}"
            shutil.make_archive(zip_name, "zip", path)

    def trimBackups():
        pass