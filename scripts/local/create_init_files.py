import os
from pathlib import Path

for folder in os.walk(".\\neon"):
    init_path = folder[0]+'\\__init__.py'
    if not any(y in folder[0] for y in ['\\env','\\.gauge', '\\log','\\resources', '\\features','\\config_files']):
       if not os.path.exists(init_path):
           Path(init_path).touch(exist_ok=False)
           print("Created init.py under:"+folder[0])
    else:
        if os.path.exists(init_path):    
            os.remove(init_path)    
            print("Deleted init.py under:"+folder[0])
        