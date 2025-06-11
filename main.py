# main.py at root

import logging
from scripts.check_deps import check_dependencies
from scripts.check_toml import TOMLValidator
import runpy
import sys

def main():
    validator = TOMLValidator()

    logging.basicConfig(level=logging.INFO)
    check_dependencies()  # custom pre-checks before running package
    settings = validator.check_toml()
    print()

    try:
        runpy.run_module("backup_manager", run_name="__main__")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
