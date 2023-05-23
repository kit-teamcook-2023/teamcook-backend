import json
from utils.backup import Backup
import atexit
from fastapi import FastAPI

app = FastAPI()

backup = Backup() # 이 경우 restore이 자동으로 발생
backup_dict = backup.notification_logs

print(backup_dict)
backup.print_dictionary()

print(backup_dict is backup.notification_logs)

backup_dict["index"] = 3
backup_dict["opo_uid1"] = {}
backup_dict["opo_uid1"]["comment"] = {}
backup_dict["opo_uid1"]["comment"]["1"] = "qwer"
backup_dict["opo_uid1"]["comment"]["2"] = "asdf"
backup_dict["opo_uid1"]["chat"] = {}
backup_dict["opo_uid1"]["chat"]["my_uid_1"] = "chatting_sended_str_1"
backup_dict["opo_uid1"]["chat"]["my_uid_2"] = "chatting_sended_str_2"

"""
logs - {
        opo_uid_1: {
            "comment": [
                "comment_append_str_1", 
                "comment_append_str_2", 
                ...
            ],
            "chat": {
                my_uid_1: "chatting_sended_str_1",
                my_uid_2: "chatting_sended_str_2",
                ...
            }
        },
        opo_uid_2: {
            "comment": [
                "comment_append_str_1", 
                "comment_append_str_2", 
                ...
            ],
            "chat": {
                my_uid_1: "chatting_sended_str_1",
                my_uid_2: "chatting_sended_str_2",
                ...
            }
        }
    }
"""

print(backup.index)
print(backup_dict)
backup.print_dictionary()

atexit.register(backup.backup_dictionary)