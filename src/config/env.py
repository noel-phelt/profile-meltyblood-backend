import os

FIREBASE = {
    'END_POINT': os.environ.get('FIREBASE_END_POINT'),
    'API_KEY': os.environ.get('FIREBASE_API_KEY')
}

GCP = {
    "project_id": os.environ.get('PROJECT_ID')
    or os.environ.get('GOOGLE_CLOUD_PROJECT')
    or os.environ.get('GCLOUD_PROJECT'),
    "bucket_name": os.environ.get('BUCKET_NAME'),
}
