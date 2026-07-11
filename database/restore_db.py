import shutil
import os

DB_FILE = "data/business.db"

BACKUP_FILE = "backup/business_backup.db"


def restore_backup():

    if not os.path.exists(BACKUP_FILE):
        return False

    shutil.copy2(BACKUP_FILE, DB_FILE)

    return True