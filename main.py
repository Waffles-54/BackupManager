# main.py at root

from scripts.check_deps import DEPValidator
from scripts.check_toml import TOMLValidator
from backup_manager.__main__ import main as backup_main
from backup_manager.logging_config import setup_logging
import sys

def main():
    """Program driver, prepares and validates the system to launch the backup_manager package"""
    logger = setup_logging()
    logger.info("Starting backup manager program")

    tomlValidator = TOMLValidator()
    depValidator = DEPValidator()
    
    try:
        depValidator.check_dependencies(logger)
        settings = tomlValidator.check_toml(logger)
        backup_main(logger, settings, argv=sys.argv[1:])
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
