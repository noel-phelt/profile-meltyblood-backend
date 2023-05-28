import os

FIREBASE = {
    'END_POINT': os.environ.get('FIREBASE_END_POINT'),
    'API_KEY': os.environ.get('FIREBASE_API_KEY')
}

FIREBASE_CERT = {
    "type": "service_account",
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('PRIVATE_KEY').replace("\\n", "\n"),
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL'),
}
GCP = {
    "project_id": os.environ.get('PROJECT_ID'),
    "bucket_name": os.environ.get('BUCKET_NAME'),
}
