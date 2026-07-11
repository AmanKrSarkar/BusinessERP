import shutil
import os

from database.database import get_connection


def create_backup():

    backup_folder = "backup"

    os.makedirs(backup_folder, exist_ok=True)

    backup_file = os.path.join(
        backup_folder,
        "business_backup.db"
    )

    shutil.copy2(DB_FILE, backup_file)

    return backup_file