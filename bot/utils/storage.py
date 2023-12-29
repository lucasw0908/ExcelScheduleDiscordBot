from ..utils.json import JsonControlor

class Storage:
        
    def get_nickname():
        return JsonControlor.get_data("nickname")
    
    def set_nickname(user: dict[str: str]) -> None:
        JsonControlor.save_data("nickname", user["id"], user["nickname"])
        
    def get_p():
        return JsonControlor.get_data("p")
    
    def set_p(user: dict[str: str]) -> None:
        JsonControlor.save_data("p", user["id"], user["p"])
        
    def find(type: str, id) -> str | None:
        
        data: dict[str: str] = JsonControlor.get_data(type)
        
        if str(id) in data.keys():
            return data[str(id)]
        else: return None