class NicknameStorage:
    
    def __init__(self) -> None:
        self._nickname = {}
        
    @property
    def nickname(self):
        return self._nickname
    
    @nickname.setter
    def nickname(self, user: dict[str: str]):
        self._nickname[user["id"]] = user["nickname"]
        
    def find(self, id) -> str | None:
        
        if id in self._nickname.keys():
            return self._nickname[id]
        else: return None
        
class PStorage:
    
    def __init__(self) -> None:
        self._p = {}
        
    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, user: dict[str: str]):
        self._p[user["id"]] = user["p"]
        
    def find(self, id) -> str | None:
        
        if id in self._p.keys():
            return self._p[id]
        else: return None
        
        
p_storage = PStorage()
nickname_storage = NicknameStorage()