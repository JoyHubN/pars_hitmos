import os
from modules import *
for name in os.listdir():
    if not name.endswith(('.py')) and not name.startswith('.'):
        for pack in os.listdir(name):
            if not "." in pack and pack not in ['__pycache__']:
                for module in  os.listdir(os.path.join(name, pack)):
                    if module.endswith('.py') and module not in ['__init__.py', '__pycache__.py']:
                        print(f'from scripts.{pack}.{module[:-3]} import *')
                        # exec(f'from scripts.{pack}.{module[:-3]} import *')