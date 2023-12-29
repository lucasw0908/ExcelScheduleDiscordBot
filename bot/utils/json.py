import json
from ..utils.module import CurrentPath

class JsonControlor:
    
    def get_data(file: str) -> dict[str: str]:
        with open(CurrentPath(f"json/{file}.json", create=True), "r") as f:
            j = json.load(f)
        return j
    
    def save_data(file: str, user_id: str, value: str):
        with open(CurrentPath(f"json/{file}.json", create=True), "r") as f:
            j = json.load(f)
            j[user_id] = value
            print(j)
        with open(CurrentPath(f"json/{file}.json", create=True), "w") as f:
            json.dump(j, f, indent=4)