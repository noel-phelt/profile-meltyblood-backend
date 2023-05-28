import firebase_admin
from firebase_admin import credentials

from config import env

cred = credentials.Certificate(env.FIREBASE_CERT)
app = firebase_admin.initialize_app(cred)


class FireBaseInit:
    def __init__(self):
        self.app = app
