from fastapi import FastAPI
import atexit
import json
from utils.backup import Backup


app = FastAPI()

backup = Backup()

backup.print_dictionary()

backup_dict = backup.notification_logs
backup_dict['test'] = 1234

print(backup_dict)
backup.print_dictionary()

backup.restore_dictionary()


atexit.register(backup.backup_dictionary)