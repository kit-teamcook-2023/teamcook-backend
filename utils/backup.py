import json

class Backup():
    def __init__(self):
        self.notification_logs = {}
        self.restore_dictionary()

    def restore_dictionary(self):
        file_path = "backup.json"
        try:
            with open(file_path, "r") as file:
                self.notification_logs = json.load(file)
        except:
            print("file not exists")

    def backup_dictionary(self):
        file_path = "backup.json"
        with open(file_path, "w") as file:
            json.dump(self.notification_logs, file)

    def print_dictionary(self):
        print(self.notification_logs)