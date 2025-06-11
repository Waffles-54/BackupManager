# scripts/check_deps.py

import importlib
import sys

REQUIRED_MODULES = [
    "os",
    "sys",
    "subprocess",
    "shutil",
    "datetime",
    "dirsync",
]

def check_dependencies():
    missing = []
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)

    if missing:
        print("Missing required modules:")
        for mod in missing:
            print(f"  - {mod}")
        print("\nPlease install all required packages with:")
        print("\tpip install -r requirements.txt")
        sys.exit(1)
    else:
        print("All required modules are installed.")

if __name__ == "__main__":
    check_dependencies()
