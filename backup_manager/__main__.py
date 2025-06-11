"""
Entry point for backup_manager package.

Allows running the package as a module with:
    python -m backup_manager
"""

import sys
import logging
import os
import tomllib 

from .prep import PrepSystem
from .core import BackupSystem

def main():
    # Setup logging config here or import logging_config if you have one
    # logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Initialize prep and core systems
    prep = PrepSystem()
    if not prep.conf_check():
        logging.error("Configuration validation failed. Exiting.")
        sys.exit(1)

    
    backup = BackupSystem()
    
    # Load the toml file
    current_dir = os.path.dirname(__file__)
    settings_path = os.path.join(current_dir, "config", "settings.toml")

    with open(settings_path, "rb") as f:
        settings = tomllib.load(f)


        

    
    # prep.arg_parser("")  # parse command-line args if needed

    # backup.sync_sys()
    # backup.bak_gen()
    # backup.bac_trimmer()

if __name__ == "__main__":
    main()
