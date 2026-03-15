import firebase_admin
from firebase_admin import credentials

from config import env

app_options = {}
if env.GCP["project_id"]:
    app_options["projectId"] = env.GCP["project_id"]

try:
    cred = credentials.ApplicationDefault()
    app = firebase_admin.initialize_app(cred, app_options or None)
except ValueError:
    app = firebase_admin.get_app()


class FireBaseInit:
    def __init__(self):
        self.app = app
