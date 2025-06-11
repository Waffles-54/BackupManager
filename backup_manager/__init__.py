"""
backup_manager package
Contains core backup management functionality.
"""

# Optional: expose main classes/functions for easy imports
from .core import BackupSystem
from .prep import PrepSystem

__all__ = ["BackupSystem", "PrepSystem"]
