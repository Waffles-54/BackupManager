# scripts/check_deps.py

import importlib
import sys

class DEPValidator:
    """Validated dependency requirements for this program"""
    def __init__(self):
        self.REQUIRED_MODULES = [
            "os",
            "sys",
            "subprocess",
            "shutil",
            "datetime",
            "dirsync",
        ]

    def check_dependencies(self, logger):
        missing = []
        for module in self.REQUIRED_MODULES:
            try:
                importlib.import_module(module)
            except ImportError:
                missing.append(module)

        if missing:
            logger.error("Missing required modules:")
            for mod in missing:
                print(f"  - {mod}")
            logger.error("\nPlease install all required packages with:")
            logger.error("pip install -r requirements.txt")
            sys.exit(1)
        else:
            logger.info("All required modules are installed.")

    if __name__ == "__main__":
        check_dependencies()
