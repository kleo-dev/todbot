from bot_token import BOT_TOKEN
from discord import Color
import json

TASK_CHANNEL=1259964210859868210

UNCOMPLETED_COLOR = Color.red()
PROGRESSING_COLOR = Color.orange()
COMPLETED_COLOR = Color.green()

# In order to change these change them in `roles.json`
class roles:
    ALLOWED_COMPLETE_PROGRESS: list[int] = []
    ALLOWED_CREATE: list[int] = []
    ALLOWED_EDIT: list[int] = []
    ALLOWED_DELETE: list[int] = []
    def load_roles():
        with open('roles.json') as f:
            data = json.load(f)
            roles.ALLOWED_CREATE=data['create']
            roles.ALLOWED_COMPLETE_PROGRESS=data['progress']
            roles.ALLOWED_EDIT=data['edit']
            roles.ALLOWED_DELETE=data['delete']