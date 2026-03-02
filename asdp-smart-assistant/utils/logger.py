import json
import os

def save_log(log):
    file_path = "chat_logs.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)