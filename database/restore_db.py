import shutil
import os

from database.database import get_connection

BACKUP_FILE = "backup/business_backup.db"


def restore_backup():

    if not os.path.exists(BACKUP_FILE):
        return False

    shutil.copy2(BACKUP_FILE, DB_FILE)

    return True