import json
from utils.backup import Backup
import atexit
from fastapi import FastAPI

app = FastAPI()

backup = Backup()

backup.restore_dictionary()
backup_dict = backup.notification_logs

print(backup_dict)
backup.print_dictionary()

print(backup_dict is backup.notification_logs)

backup_dict["qwer"] = 123456

print(backup_dict)
backup.print_dictionary()

atexit.register(backup.backup_dictionary)