import os
from pathlib import Path

class CurrentPath:
    
    def __new__(self, file: str, *, module_path: bool=False, create: bool=False) -> str | None:
        
        if module_path:
            self.path = __file__ #module file's path
        else:
            self.path = __name__ #running file's path
            
        self.curret_path = os.path.join(os.path.abspath(os.path.dirname(self.path)), file)
        
        if (not os.path.isfile(self.curret_path)) and create:
            with open(self.curret_path, "w", encoding="utf-8") as file:
                pass
            
        elif (not os.path.isfile(self.curret_path))and not create:
            raise FileNotFoundError(f'"{self.curret_path}" is not found')
            
        return self.curret_path
    
class XLSXCurrentPath(CurrentPath):
    
    def __new__(self, filename: str, *, module_path: bool=False, create: bool=False) -> str | None:
        
        if ".xlsx" not in filename:
            file = filename + ".xlsx"
        else:
            file = filename

        return super().__new__(self, file, module_path=module_path, create=create)
    
class FindAllFiles:
    
    def __new__(self, filetype: str) -> list[str]:
        return [f.stem for f in Path(os.path.abspath(os.path.dirname(__name__))).glob(f"*.{filetype}")]