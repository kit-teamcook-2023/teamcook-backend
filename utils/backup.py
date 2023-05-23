import json

class Backup():
    index = 0

    def __init__(self):
        self.notification_logs = {}
        self.restore_dictionary()

    def restore_dictionary(self):
        file_path = "backup.json"
        try:
            with open(file_path, "r") as file:
                self.notification_logs = json.load(file)
            
            self.index = self.notification_logs["index"]
        except:
            print("file not exists")
            self.index = 0

    def backup_dictionary(self):
        file_path = "backup.json"
        self.notification_logs["index"] = self.index
        with open(file_path, "w") as file:
            json.dump(self.notification_logs, file)

    def print_dictionary(self):
        print(self.notification_logs)